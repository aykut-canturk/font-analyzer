"""
Web scraping utilities for extracting font URLs from websites.
"""

import os
import re
from urllib.parse import urljoin
from typing import List, Set
import requests
from bs4 import BeautifulSoup

from font_analyzer.config.settings import (
    SUPPORTED_FONT_EXTENSIONS,
    HTTP_TIMEOUT,
)
from font_analyzer.config import settings
from font_analyzer.utils.logger import log


class WebScraper:
    """Handles web scraping operations for font detection."""

    def __init__(self, timeout: int = HTTP_TIMEOUT, verify_ssl: bool = None):
        self.timeout = timeout
        # If verify_ssl is not explicitly provided, get current value from settings
        self.verify_ssl = verify_ssl if verify_ssl is not None else settings.HTTP_VERIFY_SSL
        self._url_pattern = re.compile(r"url\(([^)]+)\)")

    def fetch_html(self, url: str) -> str:
        """
        Fetch HTML content from a URL.

        Args:
            url: The URL to fetch

        Returns:
            HTML content as string

        Raises:
            requests.RequestException: If the request fails
        """
        try:
            response = requests.get(url, verify=self.verify_ssl, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            log(f"Error fetching HTML from {url}: {e}", level="error")
            raise

    def extract_css_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract CSS URLs from <link rel="stylesheet"> tags.

        Args:
            soup: BeautifulSoup object of the HTML
            base_url: Base URL for resolving relative URLs

        Returns:
            List of absolute CSS URLs
        """
        css_links = []

        for link_tag in soup.find_all("link", rel="stylesheet"):
            href = link_tag.get("href")
            if href:
                if not href.startswith("http"):
                    href = urljoin(base_url, href)
                css_links.append(href)

        return css_links

    def extract_inline_css(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract inline CSS from <style> tags.

        Args:
            soup: BeautifulSoup object of the HTML

        Returns:
            List of CSS content strings
        """
        return [style_tag.get_text() for style_tag in soup.find_all("style")]

    def extract_font_urls_from_css(
        self, css_texts: List[str], base_url: str
    ) -> Set[str]:
        """
        Extract font URLs from CSS content.

        Args:
            css_texts: List of CSS content strings
            base_url: Base URL for resolving relative URLs

        Returns:
            Set of absolute font URLs
        """
        font_urls = set()

        for css_text in css_texts:
            matches = self._url_pattern.findall(css_text)
            for match in matches:
                font_url = match.strip("\"' ")

                # Check if it's a font file
                if any(
                    font_url.lower().endswith(ext) for ext in SUPPORTED_FONT_EXTENSIONS
                ):
                    if not font_url.startswith("http"):
                        font_url = urljoin(base_url, font_url)
                    font_urls.add(font_url)

        return font_urls

    def get_all_css_content(self, url: str) -> List[str]:
        """
        Get all CSS content from a webpage (both linked and inline).

        Args:
            url: The webpage URL

        Returns:
            List of CSS content strings
        """
        # Fetch HTML
        html_content = self.fetch_html(url)
        soup = BeautifulSoup(html_content, "html.parser")

        # Get CSS URLs
        css_urls = self.extract_css_links(soup, url)

        # Fetch CSS content
        all_css_contents = []
        for css_url in css_urls:
            try:
                css_content = self.fetch_html(css_url)
                all_css_contents.append(css_content)
            except Exception as e:
                log(f"Error fetching CSS from {css_url}: {e}", level="error")

        # Add inline CSS
        all_css_contents.extend(self.extract_inline_css(soup))

        return all_css_contents


class FontDownloader:
    """Handles font file downloading operations."""

    def __init__(self, timeout: int = HTTP_TIMEOUT, verify_ssl: bool = None):
        self.timeout = timeout
        # If verify_ssl is not explicitly provided, get current value from settings
        self.verify_ssl = verify_ssl if verify_ssl is not None else settings.HTTP_VERIFY_SSL

    def download_font_files(
        self, font_urls: Set[str], download_folder: str
    ) -> List[str]:
        """
        Download font files from URLs.

        Args:
            font_urls: Set of font URLs to download
            download_folder: Directory to save downloaded files

        Returns:
            List of paths to successfully downloaded files
        """
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        downloaded_files = []

        for font_url in font_urls:
            font_name = self._get_filename_from_url(font_url)
            font_path = os.path.join(download_folder, font_name)

            # Skip if file already exists
            if os.path.exists(font_path):
                downloaded_files.append(font_path)
                continue

            try:
                response = requests.get(
                    font_url, verify=self.verify_ssl, timeout=self.timeout
                )
                response.raise_for_status()

                with open(font_path, "wb") as f:
                    f.write(response.content)

                downloaded_files.append(font_path)
                log(f"Downloaded: {font_name}")

            except requests.RequestException as e:
                log(f"Error downloading font from {font_url}: {e}", level="error")

        return downloaded_files

    def _get_filename_from_url(self, url: str) -> str:
        """
        Extract filename from URL, removing query parameters.

        Args:
            url: The font URL

        Returns:
            Cleaned filename
        """
        return url.split("/")[-1].split("?")[0]
