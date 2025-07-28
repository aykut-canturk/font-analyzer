"""
Font metadata extraction utilities.
"""

from typing import Dict
from fontTools.ttLib import TTFont

from font_analyzer.config.settings import FONT_NAME_IDS
from font_analyzer.utils.logger import log


class FontMetadataExtractor:
    """Extracts and processes font metadata."""

    @staticmethod
    def extract_metadata(font: TTFont) -> Dict[int, str]:
        """
        Extract metadata from a TTFont object's name table.

        Args:
            font: The TTFont object to extract metadata from

        Returns:
            Dictionary mapping name IDs to their string values
        """
        metadata = {}

        try:
            name_table = font["name"]

            for record in name_table.names:
                name_id = record.nameID
                value = record.string

                # Handle different encodings
                try:
                    if b"\000" in value:
                        value = value.decode("utf-16-be")
                    else:
                        value = value.decode("utf-8")
                except UnicodeDecodeError:
                    try:
                        value = value.decode("latin1")
                    except UnicodeDecodeError:
                        # If all else fails, use repr to show raw bytes
                        value = repr(value)

                metadata[name_id] = value

        except Exception as e:
            log(f"Error extracting font metadata: {e}", level="error")

        return metadata

    @staticmethod
    def get_font_family_name(metadata: Dict[int, str]) -> str:
        """
        Extract font family name from metadata.

        Priority order:
        1. Font Family name (nameID 1)
        2. Full font name (nameID 4)
        3. PostScript name (nameID 6)

        Args:
            metadata: Font metadata dictionary

        Returns:
            Font family name or empty string if not found
        """
        for name_id in [
            FONT_NAME_IDS["FAMILY"],
            FONT_NAME_IDS["FULL_NAME"],
            FONT_NAME_IDS["POSTSCRIPT"],
        ]:
            if name_id in metadata and metadata[name_id]:
                return metadata[name_id]

        return ""

    @staticmethod
    def process_font_file(font_path: str) -> Dict[int, str]:
        """
        Process a single font file and extract its metadata.

        Args:
            font_path: Path to the font file

        Returns:
            Dictionary containing font metadata
        """
        try:
            font = TTFont(font_path)
            return FontMetadataExtractor.extract_metadata(font)
        except Exception as e:
            log(f"Error processing font file {font_path}: {e}", level="error")
            return {}
