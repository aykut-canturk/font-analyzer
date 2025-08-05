# 🎨 Font Analyzer

Automated font discovery, analysis, and compliance validation from websites and local files.

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/font-analyzer.svg)](https://pypi.org/project/font-analyzer/)

## Features

- 🌐 Discover fonts from websites
- 📁 Analyze local font files
- ✅ Validate against custom whitelist policies
- 📊 Generate compliance reports
- 🔧 Support for TTF, OTF, WOFF, WOFF2 formats

## Installation

```bash
pip install font-analyzer
```

## Quick Start

### Analyze Website Fonts

```bash
font-analyzer --url "https://github.com" --allowed_fonts "Roboto" "Arial" "Open Sans"
```

### Analyze Local Font File

```bash
font-analyzer --font_path "./fonts/my-font.ttf" --allowed_fonts "Roboto" "Arial"
```

## Usage Examples

### Basic Commands

```bash
# Website analysis
font-analyzer --url "https://github.com"

# Local file analysis  
font-analyzer --font_path "/path/to/font.ttf"

# With whitelist validation
font-analyzer --url "https://github.com" --allowed_fonts "Roboto" ".*Arial.*"

# Verbose output for detailed analysis
font-analyzer --url "https://github.com" --verbose
# or use short form
font-analyzer --url "https://github.com" -v

# Get help and see all options
font-analyzer --help
```

### Environment Variables

```bash
# Set environment variables
export URL="https://github.com"
export ALLOWED_FONTS="Roboto,Open Sans,.*Arial.*"
font-analyzer

# Windows
set ALLOWED_FONTS=Roboto,Open Sans,.*Arial.*
font-analyzer
```

## Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `URL` | Website URL to analyze | `https://github.com` |
| `FONT_PATH` | Path to font file | `./fonts/font.ttf` |
| `ALLOWED_FONTS` | Comma-separated font patterns | `Roboto,Arial,.*Sans.*` |

## 📄 License

MIT License

## 🔗 Links

- [GitHub](https://github.com/aykut-canturk/font-analyzer)
- [Bug Reports](https://github.com/aykut-canturk/font-analyzer/issues)
