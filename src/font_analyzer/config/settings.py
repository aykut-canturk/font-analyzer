"""
Configuration settings for font analyzer.
"""

# Default download folder for font files
# Use /app/fonts in Docker container, temporary folder in local development
import os
import tempfile

if os.path.exists("/app"):
    DEFAULT_DOWNLOAD_FOLDER = "/app/fonts"
else:
    # tmp folder for local development
    DEFAULT_DOWNLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "font-analyzer-fonts")

# Supported font file extensions
SUPPORTED_FONT_EXTENSIONS = [".woff", ".woff2", ".ttf", ".otf"]


timeout = os.getenv("HTTP_TIMEOUT", "1")

# HTTP request settings
HTTP_TIMEOUT = int(timeout) if timeout.isdigit() else 1
HTTP_VERIFY_SSL = os.getenv("VERIFY_SSL", "1") == "1"

# Font name IDs for metadata extraction
FONT_NAME_IDS = {
    "FAMILY": 1,  # Font Family name
    "FULL_NAME": 4,  # Full font name
    "POSTSCRIPT": 6,  # PostScript name
}
