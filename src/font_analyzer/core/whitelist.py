"""
Whitelist management for font validation.
"""

import os
import re
from typing import List, Optional
from importlib import resources as pkg_resources
import yaml

from colorama import Fore, Style

from font_analyzer.config.settings import WHITELIST_PATHS
from font_analyzer.utils.logger import log


class WhitelistManager:
    """Manages font whitelist patterns and validation."""

    def __init__(self, whitelist_path: Optional[str] = None):
        self._allowed_patterns: List[str] = []
        self._load_whitelist(whitelist_path)

    def _load_whitelist(self, custom_path: Optional[str] = None) -> None:
        """Load whitelist patterns from configuration files."""

        # If custom path is provided, try it first
        if custom_path and os.path.exists(custom_path):
            self._load_from_file(custom_path)
            log(f"Whitelist loaded from custom path: {custom_path}")
            return

        # Otherwise, try default paths
        for path in WHITELIST_PATHS:
            if os.path.exists(path):
                self._load_from_file(path)
                log(f"Whitelist loaded from: {path}")
                return

        if pkg_resources.is_resource("font_analyzer", "whitelist.yaml"):
            # Load from package resource if available
            with pkg_resources.open_text(
                "font_analyzer", "whitelist.yaml"
            ) as f:
                self._load_from_file(f.name)
            log(
                "Whitelist loaded from package resource: "
                "font_analyzer/whitelist.yaml"
            )
            return

        raise FileNotFoundError(
            f"{Fore.RED}Warning: No whitelist file found in paths: {', '.join(WHITELIST_PATHS)}{Style.RESET_ALL}"
        )

    def _load_from_file(self, file_path: str) -> None:
        """Load patterns from a YAML whitelist file."""
        patterns = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and "font_whitelist" in data:
                    for idx, pattern in enumerate(data["font_whitelist"], 1):
                        if not pattern:
                            continue
                        try:
                            re.compile(pattern)
                            patterns.append(pattern)
                        except re.error:
                            log(
                                f"{Fore.YELLOW}Warning: Invalid regex pattern at index {idx}: {pattern} - using as plain text{Style.RESET_ALL}"
                            )
                            patterns.append(re.escape(pattern))
                else:
                    log(
                        f"{Fore.RED}Warning: 'whitelist' key not found in YAML file: {file_path}{Style.RESET_ALL}"
                    )
            self._allowed_patterns = patterns
        except Exception as e:
            log(f"Error loading whitelist from {file_path}: {e}", level="error")
            self._allowed_patterns = []

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
        """Reload whitelist patterns from files."""
        self._load_whitelist()
