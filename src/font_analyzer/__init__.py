"""
Font Detector Package - Core functionality for font analysis and validation.
"""

__version__ = "0.0.5"
__author__ = "Aykut Cantürk"
__description__ = "A tool for detecting and validating fonts from websites and files"

from .core.analyzer import FontAnalyzer
from .core.metadata import FontMetadataExtractor
from .core.whitelist import WhitelistManager

__all__ = ["FontAnalyzer", "FontMetadataExtractor", "WhitelistManager"]
