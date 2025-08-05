"""
Whitelist management for font validation.
"""

import os
import re
from typing import List, Optional

from colorama import Fore, Style

from font_analyzer.utils.logger import log


class WhitelistManager:
    """Manages font whitelist patterns and validation."""

    def __init__(
        self,
        allowed_fonts: Optional[List[str]] = None,
    ):
        self._allowed_patterns: List[str] = []

        # Add patterns from direct array parameter
        if allowed_fonts:
            self._add_patterns_from_array(allowed_fonts)
        else:
            # Load from .env file if no allowed_fonts provided
            self._load_from_env()

        # Raise error if no patterns loaded
        if not self._allowed_patterns:
            raise RuntimeError(
                f"{Fore.RED}WhitelistManager initialized with no patterns. "
                "Parameters must include allowed_fonts or set ALLOWED_FONTS "
                f"environment variable.{Style.RESET_ALL}"
            )

        # Log all loaded patterns
        log(
            f"Loaded {len(self._allowed_patterns)} whitelist patterns: "
            f"{', '.join(self._allowed_patterns)}"
        )

    def _load_from_env(self) -> None:
        """Load whitelist patterns from .env file."""
        from dotenv import load_dotenv

        # Load .env file
        load_dotenv()

        # Get ALLOWED_FONTS from environment
        env_allowed_fonts = os.getenv("ALLOWED_FONTS")

        if env_allowed_fonts:
            # Parse comma-separated fonts
            fonts_list = [
                font.strip() for font in env_allowed_fonts.split(",") if font.strip()
            ]
            if fonts_list:
                self._add_patterns_from_array(fonts_list)
                log(f"Fonts loaded from .env file: {len(fonts_list)} patterns")
            else:
                log("No valid fonts found in .env ALLOWED_FONTS")
        else:
            log("No ALLOWED_FONTS found in .env file")

    def _add_patterns_from_array(self, allowed_fonts: List[str]) -> None:
        """Add patterns from an array of allowed fonts."""
        additional_patterns = []
        for font in allowed_fonts:
            if not font:
                continue
            try:
                # Test if it's a valid regex pattern
                re.compile(font)
                additional_patterns.append(font)
            except re.error:
                # If not a valid regex, escape it to be treated as literal text
                escaped_pattern = re.escape(font)
                additional_patterns.append(escaped_pattern)
                log(f"Added escaped font pattern: {escaped_pattern}")

        # Add to existing patterns
        self._allowed_patterns.extend(additional_patterns)

    def is_font_allowed(self, font_name: str) -> bool:
        """
        Check if a font name is allowed based on whitelist patterns.

        Args:
            font_name: The font name to check

        Returns:
            True if font is allowed, False otherwise
        """
        if not self._allowed_patterns:
            return True  # No restrictions if whitelist is empty

        if not font_name:
            return False

        normalized_name = self._normalize_font_name(font_name)

        # Check against each whitelist pattern
        for pattern in self._allowed_patterns:
            try:
                if re.search(pattern, normalized_name, re.IGNORECASE):
                    return True
            except re.error:
                # Fallback to exact string match
                if pattern.lower() == normalized_name:
                    return True

        return False

    def get_matching_pattern(self, font_name: str) -> Optional[str]:
        """
        Get the whitelist pattern that matches the given font name.

        Args:
            font_name: The font name to check

        Returns:
            The matching pattern or None if no match found
        """
        if not font_name or not self._allowed_patterns:
            return None

        normalized_name = self._normalize_font_name(font_name)

        for pattern in self._allowed_patterns:
            try:
                if re.search(pattern, normalized_name, re.IGNORECASE):
                    return pattern
            except re.error:
                if pattern.lower() == normalized_name:
                    return pattern

        return None

    def _normalize_font_name(self, font_name: str) -> str:
        """
        Normalize font name for comparison.

        Args:
            font_name: The original font name

        Returns:
            Normalized font name
        """
        normalized = font_name.lower().strip()

        # Remove file extensions
        if normalized.endswith((".ttf", ".otf", ".woff", ".woff2")):
            normalized = normalized.rsplit(".", 1)[0]

        return normalized

    @property
    def pattern_count(self) -> int:
        """Get the number of loaded patterns."""
        return len(self._allowed_patterns)

    def reload(self) -> None:
        """Reload whitelist patterns from .env file."""
        self._allowed_patterns = []
        self._load_from_env()
