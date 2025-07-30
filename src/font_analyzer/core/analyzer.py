"""
Font analysis and validation functionality.
"""

import os
import time
from typing import Dict, List, NamedTuple, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from colorama import Fore, Style

from font_analyzer.utils.web_scraper import WebScraper, FontDownloader
from font_analyzer.core.metadata import FontMetadataExtractor
from font_analyzer.core.whitelist import WhitelistManager
from font_analyzer.config.settings import DEFAULT_DOWNLOAD_FOLDER
from font_analyzer.utils.logger import log


@dataclass
class FontAnalysisResult:
    """Result of font analysis containing validation information."""

    font_path: str
    font_name: str
    font_family: str
    metadata: Dict[int, str]
    is_allowed: bool
    matching_pattern: Optional[str] = None
    file_size: Optional[int] = None
    analysis_time: Optional[float] = None


class FontSummary(NamedTuple):
    """Summary of font analysis results."""

    found_fonts: List[str]
    allowed_fonts: List[str]
    disallowed_fonts: List[str]
    all_fonts_allowed: bool
    total_analysis_time: float


class FontAnalyzer:
    """Main class for analyzing fonts and validating against whitelist."""

    def __init__(
        self,
        max_workers: int = 4,
        whitelist_path: Optional[str] = None,
        allowed_fonts: Optional[List[str]] = None,
    ):
        self.whitelist_manager = WhitelistManager(
            whitelist_path=whitelist_path, allowed_fonts=allowed_fonts
        )
        self.metadata_extractor = FontMetadataExtractor()
        self.web_scraper = WebScraper()
        self.font_downloader = FontDownloader()
        self.max_workers = max_workers

    def _analyze_font_with_timing(self, font_path: str) -> FontAnalysisResult:
        """Analyze a font file with timing information."""
        start_time = time.time()

        try:
            # Get file size
            file_size = (
                os.path.getsize(font_path) if os.path.exists(font_path) else None
            )

            # Perform analysis
            result = self._analyze_single_font(font_path)

            # Add timing and size information
            result.file_size = file_size
            result.analysis_time = time.time() - start_time

            return result

        except Exception as e:
            log(f"{Fore.RED}Error analyzing {font_path}: {str(e)}{Style.RESET_ALL}")
            # Return a minimal result with error information
            return FontAnalysisResult(
                font_path=font_path,
                font_name=os.path.basename(font_path),
                font_family="Unknown",
                metadata={},
                is_allowed=False,
                matching_pattern=None,
                file_size=file_size if "file_size" in locals() else None,
                analysis_time=time.time() - start_time,
            )

    def analyze_multiple_fonts(self, font_paths: List[str]) -> List[FontAnalysisResult]:
        """Analyze multiple font files concurrently."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all font analysis tasks
            future_to_path = {
                executor.submit(self._analyze_font_with_timing, path): path
                for path in font_paths
            }

            # Collect results as they complete
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    log(f"{Fore.RED}Error processing {path}: {str(e)}{Style.RESET_ALL}")
                    # Add error result
                    results.append(
                        FontAnalysisResult(
                            font_path=path,
                            font_name=os.path.basename(path),
                            font_family="Error",
                            metadata={},
                            is_allowed=False,
                            matching_pattern=None,
                        )
                    )

        return results

    def analyze_website_fonts(
        self, url: str, download_folder: str = DEFAULT_DOWNLOAD_FOLDER
    ) -> List[FontAnalysisResult]:
        """
        Analyze fonts from a website.

        Args:
            url: The website URL to analyze
            download_folder: Directory to save downloaded fonts

        Returns:
            List of FontAnalysisResult objects
        """
        log(f"Scraping fonts from URL: {url}")

        try:
            # Get all CSS content with URLs
            css_content_with_urls = self.web_scraper.get_all_css_content(url)

            # Extract font URLs
            font_urls = self.web_scraper.extract_font_urls_from_css(
                css_content_with_urls
            )

            if not font_urls:
                log("No font URLs found in CSS")
                return []

            # Download fonts
            downloaded_files = self.font_downloader.download_font_files(
                font_urls, download_folder
            )

            if not downloaded_files:
                log("No font files were successfully downloaded")
                return []

            # Analyze each font
            results = []
            for font_path in downloaded_files:
                result = self._analyze_single_font(font_path)
                if result:
                    results.append(result)

            return results

        except requests.RequestException as e:
            log(f"Network error analyzing website fonts: {e}", level="error")
            return []
        except Exception as e:
            log(f"Error analyzing website fonts: {e}", level="error")
            return []

    def analyze_single_font_file(self, font_path: str) -> FontAnalysisResult:
        """
        Analyze a single font file.

        Args:
            font_path: Path to the font file

        Returns:
            FontAnalysisResult object or None if analysis fails
        """
        if not os.path.exists(font_path):
            log(f"Font file does not exist: {font_path}", level="error")
            return None

        return self._analyze_single_font(font_path)

    def _analyze_single_font(self, font_path: str) -> FontAnalysisResult:
        """
        Internal method to analyze a single font file.

        Args:
            font_path: Path to the font file

        Returns:
            FontAnalysisResult object or None if analysis fails
        """
        try:
            # Extract metadata
            metadata = self.metadata_extractor.process_font_file(font_path)
            if not metadata:
                return None

            # Get font names
            font_name = os.path.basename(font_path)
            font_family = self.metadata_extractor.get_font_family_name(metadata)

            # Check if font is allowed
            font_family_allowed = self.whitelist_manager.is_font_allowed(font_family)
            filename_allowed = self.whitelist_manager.is_font_allowed(
                font_name.replace(".ttf", "").replace(".otf", "")
            )
            is_allowed = font_family_allowed or filename_allowed

            # Get matching pattern
            matching_pattern = None
            if font_family_allowed:
                matching_pattern = self.whitelist_manager.get_matching_pattern(
                    font_family
                )
            elif filename_allowed:
                matching_pattern = self.whitelist_manager.get_matching_pattern(
                    font_name.replace(".ttf", "").replace(".otf", "")
                )

            return FontAnalysisResult(
                font_path=font_path,
                font_name=font_name,
                font_family=font_family,
                metadata=metadata,
                is_allowed=is_allowed,
                matching_pattern=matching_pattern,
            )

        except Exception as e:
            log(f"Error analyzing font {font_path}: {e}", level="error")
            return None

    def generate_summary(self, results: List[FontAnalysisResult]) -> FontSummary:
        """
        Generate a summary of font analysis results.

        Args:
            results: List of FontAnalysisResult objects

        Returns:
            FontSummary object
        """
        found_fonts = []
        allowed_fonts = []
        disallowed_fonts = []

        for result in results:
            display_name = (
                result.font_family if result.font_family else result.font_name
            )
            found_fonts.append(display_name)

            if result.is_allowed:
                allowed_fonts.append(display_name)
            else:
                disallowed_fonts.append(display_name)

        all_fonts_allowed = len(disallowed_fonts) == 0

        total_analysis_time = sum(
            result.analysis_time
            for result in results
            if result.analysis_time is not None
        )

        return FontSummary(
            found_fonts=list(set(found_fonts)) if found_fonts else [],
            allowed_fonts=(list(set(allowed_fonts)) if allowed_fonts else []),
            disallowed_fonts=(list(set(disallowed_fonts)) if disallowed_fonts else []),
            all_fonts_allowed=all_fonts_allowed,
            total_analysis_time=total_analysis_time,
        )

    def log_results(self, results: List[FontAnalysisResult]) -> None:
        """
        Log detailed analysis results.

        Args:
            results: List of FontAnalysisResult objects
        """
        for result in results:
            self._log_single_result(result)

        # Log overall status
        summary = self.generate_summary(results)
        if summary.all_fonts_allowed:
            log(f"\n{Fore.GREEN}✓ All fonts are in the whitelist.{Style.RESET_ALL}")
        else:
            log(f"\n{Fore.RED}✗ Some fonts are not in the whitelist!{Style.RESET_ALL}")

    def _log_single_result(self, result: FontAnalysisResult) -> None:
        """
        Log results for a single font.

        Args:
            result: FontAnalysisResult object
        """
        display_name = result.font_family if result.font_family else result.font_name

        if result.is_allowed:
            status = f"{Fore.GREEN}✓ ALLOWED"
            pattern_info = (
                f" (pattern: {Fore.CYAN}{result.matching_pattern}{Fore.GREEN})"
                if result.matching_pattern
                else ""
            )
            log(
                f"\n=== Metadata for {result.font_name} ({display_name}) === {status}{pattern_info}{Style.RESET_ALL}",
                level="debug",
            )
        else:
            status = f"{Fore.RED}✗ NOT ALLOWED"
            log(
                f"\n=== Metadata for {result.font_name} ({display_name}) === {status}{Style.RESET_ALL}",
                level="debug",
            )

        # Log metadata
        for name_id, value in result.metadata.items():
            log(f"NameID {name_id}: {value}", level="debug")
