#!/usr/bin/env python3
"""
Example unit tests for the refactored font analyzer.

This demonstrates how the modular structure makes testing easier.
Run with: python -m pytest tests/test_font_analyzer.py -v
"""
import unittest
import sys
import os
from pathlib import Path
from unittest.mock import patch

# Add src to path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

from font_analyzer.core.whitelist import WhitelistManager
from font_analyzer.core.metadata import FontMetadataExtractor


class TestWhitelistManager(unittest.TestCase):
    """Test cases for WhitelistManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = WhitelistManager()

    @patch.dict(os.environ, {"ALLOWED_FONTS": "roboto,lato,open.*sans"}, clear=True)
    def test_load_whitelist_success(self):
        """Test successful whitelist loading from .env."""
        manager = WhitelistManager()
        self.assertEqual(manager.pattern_count, 3)

    def test_allowed_fonts_parameter(self):
        """Test initialization with allowed_fonts parameter."""
        allowed_fonts = ["Roboto", "Open Sans", "Arial.*"]
        manager = WhitelistManager(allowed_fonts=allowed_fonts)
        self.assertEqual(manager.pattern_count, 3)
        
        # Test that fonts are properly allowed
        self.assertTrue(manager.is_font_allowed("Roboto"))
        self.assertTrue(manager.is_font_allowed("Open Sans"))
        self.assertTrue(manager.is_font_allowed("Arial Bold"))

    def test_normalize_font_name(self):
        """Test font name normalization."""
        # Test the private method through is_font_allowed
        test_cases = [
            ("Roboto-Regular.ttf", "roboto"),
            ("Lato Bold.otf", "lato bold"),
            ("OpenSans.woff2", "opensans"),
            ("HELVETICA", "helvetica"),
        ]

        # Set up a simple pattern for testing
        self.manager._allowed_patterns = ["roboto", "lato", "opensans"]

        for font_name, expected_base in test_cases:
            # Test that normalization works correctly
            result = self.manager.is_font_allowed(font_name)
            expected = any(
                pattern in expected_base for pattern in self.manager._allowed_patterns
            )
            self.assertEqual(result, expected, f"Failed for {font_name}")

    def test_font_allowed_patterns(self):
        """Test font pattern matching."""
        # Set up test patterns
        self.manager._allowed_patterns = ["roboto", "lato.*", "open.*sans"]

        test_cases = [
            ("Roboto", True),
            ("Roboto-Bold", True),
            ("Lato", True),
            ("Lato-Italic", True),
            ("OpenSans", True),
            ("Open Sans", True),
            ("Helvetica", False),
            ("Arial", False),
        ]

        for font_name, expected in test_cases:
            result = self.manager.is_font_allowed(font_name)
            self.assertEqual(result, expected, f"Failed for {font_name}")

    def test_get_matching_pattern(self):
        """Test getting the specific pattern that matches."""
        self.manager._allowed_patterns = ["roboto", "lato.*bold"]

        self.assertEqual(self.manager.get_matching_pattern("Roboto"), "roboto")
        self.assertEqual(self.manager.get_matching_pattern("Lato-Bold"), "lato.*bold")
        self.assertIsNone(self.manager.get_matching_pattern("Helvetica"))


class TestFontMetadataExtractor(unittest.TestCase):
    """Test cases for FontMetadataExtractor class."""

    def test_get_font_family_name(self):
        """Test font family name extraction priority."""
        extractor = FontMetadataExtractor()

        # Test priority: nameID 1 (family) > 4 (full) > 6 (postscript)
        metadata_cases = [
            ({1: "Roboto", 4: "Roboto Regular", 6: "Roboto-Regular"}, "Roboto"),
            ({4: "Lato Bold", 6: "Lato-Bold"}, "Lato Bold"),
            ({6: "Helvetica-Neue"}, "Helvetica-Neue"),
            ({}, ""),
            ({2: "Regular"}, ""),  # Wrong nameID
        ]

        for metadata, expected in metadata_cases:
            result = extractor.get_font_family_name(metadata)
            self.assertEqual(result, expected)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components."""

    @patch.dict(os.environ, {"ALLOWED_FONTS": "roboto,lato,open.*sans"}, clear=True)
    def test_whitelist_integration(self):
        """Test that whitelist manager integrates correctly."""
        manager = WhitelistManager()
        # Should load from .env file
        self.assertEqual(manager.pattern_count, 3)

        # Test font validation
        self.assertTrue(manager.is_font_allowed("Roboto"))
        self.assertTrue(manager.is_font_allowed("lato"))
        self.assertTrue(manager.is_font_allowed("Open Sans"))
        self.assertFalse(manager.is_font_allowed("Times New Roman"))


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
