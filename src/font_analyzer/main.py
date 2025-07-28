#!/usr/bin/env python3
"""
Font Analyzer - Main entry point.

Usage: python main.py --url "https://www.example.com"
       python main.py --font_path "/path/to/font.ttf"
"""
import argparse
import os
import sys
from colorama import init, Fore, Style

from font_analyzer.core.analyzer import FontAnalyzer
from font_analyzer.utils.logger import log
from font_analyzer.utils.formatter import print_summary
from font_analyzer.config import settings

# Initialize colorama for colored output in terminal
init()


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Font Analyzer - Analyze fonts from websites or files"
    )
    parser.add_argument(
        "--url", help="URL of a website to scrape all fonts from (HTML + CSS)"
    )
    parser.add_argument("--font_path", help="Path to a single font file")
    parser.add_argument("--whitelist_path", help="Path to custom whitelist file")
    parser.add_argument(
        "--allowed_fonts",
        nargs="*",
        help="List of allowed font patterns (can use regex patterns)",
    )
    parser.add_argument(
        "--verify-ssl",
        type=int,
        choices=[0, 1],
        default=1,
        help="Enable SSL verification for HTTP requests (1=enabled, 0=disabled, default=1)",
    )
    return parser


def main() -> int:
    """Main entry point of the application."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Check for environment variables if no arguments provided
    if not args.url and not args.font_path:
        env_url = os.getenv("URL")
        env_font_path = os.getenv("FONT_PATH")
        env_whitelist_path = os.getenv("WHITELIST_PATH")
        env_allowed_fonts = os.getenv("ALLOWED_FONTS")

        if env_url:
            args.url = env_url
        elif env_font_path:
            args.font_path = env_font_path

        if env_whitelist_path and not args.whitelist_path:
            args.whitelist_path = env_whitelist_path

        # Parse allowed fonts from environment variable (comma-separated)
        if env_allowed_fonts and not args.allowed_fonts:
            args.allowed_fonts = [
                font.strip() for font in env_allowed_fonts.split(",") if font.strip()
            ]

    # Update SSL verification setting based on argument
    settings.HTTP_VERIFY_SSL = bool(args.verify_ssl)

    # Validate arguments
    if not args.url and not args.font_path:
        parser.print_help()
        print("\nError: Either provide --font_path or --url to scrape from a website.")
        print("You can also set URL or FONT_PATH environment variables.")
        print("\nAdditional options:")
        print("  --allowed_fonts: Specify allowed font patterns directly as parameters")
        print("  ALLOWED_FONTS: Environment variable for comma-separated allowed fonts")
        return 1

    # Initialize font analyzer
    analyzer = FontAnalyzer(
        whitelist_path=args.whitelist_path, allowed_fonts=args.allowed_fonts
    )

    try:
        results = []

        # Process website fonts
        if args.url:
            results = analyzer.analyze_website_fonts(args.url)
            if not results:
                log("No font files found or processed from the website.")
                return 1

        # Process single font file
        elif args.font_path:
            log(f"Processing single font file: {args.font_path}")
            result = analyzer.analyze_single_font_file(args.font_path)
            if result:
                results = [result]
            else:
                log("Failed to process the font file.")
                return 1

        # Log detailed results
        analyzer.log_results(results)

        # Generate and print summary
        summary = analyzer.generate_summary(results)
        print_summary(summary, results)

        # Final status message
        print(f"\n{Fore.BLUE}Operation completed successfully.{Style.RESET_ALL}")

        # Return appropriate exit code
        return 0 if summary.all_fonts_allowed else 1

    except KeyboardInterrupt:
        log("\nOperation cancelled by user.")
        return 130
    except Exception as e:
        log(f"Unexpected error: {e}", level="error")
        return 1


if __name__ == "__main__":
    # Run the main function and exit with the appropriate code
    sys.exit(main())
