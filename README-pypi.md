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

## 🚀 Usage

Analyze fonts from a website:

```sh
font-analyzer --url "https://github.com"
```

Analyze a local font file:

```sh
font-analyzer --font_path "/path/to/fontfile"
```

Use a custom whitelist:

```sh
font-analyzer --url "https://github.com" --whitelist_path "/path/to/whitelist.yaml"
```

Disable SSL verification (for testing or non-SSL endpoints):

```sh
font-analyzer --url "https://github.com" --verify-ssl 0
```

## ⚙️ Configuration

Environment variables:
- `URL`: Website to analyze
- `FONT_PATH`: Path to font file
- `WHITELIST_PATH`: Path to whitelist YAML
- `VERIFY_SSL`: Set to `0` to disable SSL verification

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
