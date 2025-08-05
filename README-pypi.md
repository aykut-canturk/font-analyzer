# 🎨 Font Analyzer

Font Analyzer is a Python CLI and API for automated font discovery, analysis, and compliance validation from websites and local files. It provides a unified workflow for font metadata extraction, policy-based validation, and reporting, making it ideal for compliance, licensing, and security use cases.

[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)](https://github.com/aykut-canturk/font-analyzer)

## 🚀 Project Highlights

- 🌐 Website font discovery and download
- 📋 Extract font family, style, license, and more
- ✅ Validate fonts against custom regex-based policies (whitelist)
- 🔧 Supports TTF, OTF, WOFF, WOFF2, and other formats
- 📊 Color-coded compliance reports
- 📝 Structured logging and flexible configuration
- 🐳 Docker & Docker Compose support

## 🛠️ The Font Analysis Pipeline

Font Analyzer follows a typical pipeline for font compliance:

1. 🌐 Discover fonts from websites or local files
2. 📋 Extract and analyze font metadata
3. ✅ Validate fonts against whitelist policies
4. 📊 Generate compliance reports
5. ⚙️ Integrate with CI/CD or enterprise workflows

## 📦 Setup

Install the latest release from PyPI:

```sh
pip install font-analyzer
```

Or for development:

```sh
git clone https://github.com/aykut-canturk/font-analyzer.git
cd font-analyzer
pip install -e .
```

## 🚀 Quick Start

### 📦 Global Installation

```bash
# Clone and install
git clone https://github.com/aykut-canturk/font-analyzer.git
cd font-analyzer
pip install -r requirements.txt

# Run font-analyzer
font-analyzer --url "https://github.com"
font-analyzer --font_path "/path/to/font.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
font-analyzer --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

### ⚡ UV Development Environment

```bash
# Run with uvicorn
uv run python -m font_analyzer.main --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
uv run python -m font_analyzer.main --font_path "/path/to/font.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

### 🐳 Docker Usage

```bash
# Basic usage
docker run --rm font-analyzer --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"

# Mount local fonts directory
docker run --rm -v "/path/to/fonts:/app/fonts" font-analyzer --font_path "/app/fonts/Roboto-Regular.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

### 🐍 Traditional Python

```bash
# Directly using Python
python -m font_analyzer.main --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
python -m font_analyzer.main --font_path "/path/to/font.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

---

## Usage Examples

### Website Font Analysis

```bash
font-analyzer --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
uv run python -m font_analyzer.main --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

### Local Font File Analysis

```bash
font-analyzer --font_path "/path/to/font.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
uv run python -m font_analyzer.main --font_path "/path/to/font.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

### Docker Usage

```bash
docker run --rm font-analyzer --url "https://github.com" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
docker run --rm -v "/path/to/fonts:/app/fonts" font-analyzer --font_path "/app/fonts/Roboto-Regular.ttf" --allowed_fonts "Roboto" "Open Sans" ".*Arial.*"
```

### Environment Variable Usage

```bash
# Windows
set ALLOWED_FONTS=Roboto,Open Sans,.*Arial.*
set FONT_PATH=fonts/my-font.ttf
font-analyzer

# Linux/macOS
export ALLOWED_FONTS=Roboto,Open Sans,.*Arial.*
export FONT_PATH=fonts/my-font.ttf
font-analyzer
```

---

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `URL` | Website URL to analyze | `https://github.com` |
| `FONT_PATH` | Path to font file | `./fonts/font.woff` |
| `ALLOWED_FONTS` | Comma-separated list of allowed font patterns | `Roboto,Open Sans,.*Arial.*` |

## 👨‍💻 Development

To release a new version:

1. ✏️ Update the version in `src/font_analyzer/__init__.py`
2. ⬆️ Commit and push changes
3. 🏷️ Tag the release: `git tag v<version>`
4. 🚀 Push tags: `git push --tags`
5. ✅ Verify build and release on PyPI

## 📄 License

MIT License

## 🔗 Links

- [GitHub](https://github.com/aykut-canturk/font-analyzer)
- [Bug Reports](https://github.com/aykut-canturk/font-analyzer/issues)
