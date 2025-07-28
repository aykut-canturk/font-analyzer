#!/usr/bin/env python3
"""
Font Analyzer - Output formatting utilities.

This module contains functions for formatting and displaying analysis results
in a visually appealing way with colors, emojis, and proper alignment.
"""
from colorama import Fore, Style


def _print_table_row(
    label: str, value: str, color: str = Fore.WHITE, label_width: int = 25
) -> None:
    """Print a single row in the summary table with proper formatting."""
    # Calculate remaining space for perfect alignment
    remaining_space = 48 - label_width - len(value) - 2  # 2 for spaces around value

    print(
        f"{Fore.CYAN}║{Style.RESET_ALL} {color}{label:<{label_width}}{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}{value}{Style.RESET_ALL}{' ' * remaining_space} {Fore.CYAN}║{Style.RESET_ALL}"
    )


def _print_table_header(title: str) -> None:
    """Print the table header with decorative border."""
    print(f"\n{Fore.CYAN}╔{'═' * 50}╗{Style.RESET_ALL}")
    print(
        f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}{title:^49}{Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}"
    )
    print(f"{Fore.CYAN}╠{'═' * 50}╣{Style.RESET_ALL}")


def _print_table_footer() -> None:
    """Print the table footer."""
    print(f"{Fore.CYAN}╚{'═' * 50}╝{Style.RESET_ALL}")


def _print_status_row(summary) -> None:
    """Print the status row in the summary table."""
    print(f"{Fore.CYAN}╠{'═' * 50}╣{Style.RESET_ALL}")

    if summary.all_fonts_allowed:
        status_color = Fore.GREEN
        status_icon = "✅"
        status_text = "ALL FONTS COMPLIANT"
    else:
        status_color = Fore.RED
        status_icon = "⚠️"
        status_text = "COMPLIANCE ISSUES FOUND"

    print(
        f"{Fore.CYAN}║{Style.RESET_ALL} {status_color}{Style.BRIGHT}{status_icon} STATUS: {status_text:<37}{Style.RESET_ALL} {Fore.CYAN}║{Style.RESET_ALL}"
    )


def _print_font_list(
    title: str, fonts: list, color: str, icon: str, empty_message: str
) -> None:
    """Print a formatted list of fonts with proper styling."""
    print(f"\n{color}{icon} {title}:{Style.RESET_ALL}")

    if fonts:
        for i, font in enumerate(fonts, 1):
            print(f"  {color}{i:2d}. {font}{Style.RESET_ALL}")
    else:
        print(f"  {Fore.YELLOW}{empty_message}{Style.RESET_ALL}")


def _calculate_compliance_rate(summary) -> float:
    """Calculate the compliance rate percentage."""
    total_found = len(summary.found_fonts)
    total_allowed = len(summary.allowed_fonts)
    return (total_allowed / total_found) * 100 if total_found > 0 else 0


def _create_progress_bar(percentage: float, length: int = 30) -> str:
    """Create a colored progress bar for the compliance rate."""
    filled_length = int(length * percentage / 100)
    bar_color = (
        Fore.GREEN
        if percentage >= 80
        else Fore.YELLOW if percentage >= 50 else Fore.RED
    )
    return f"{bar_color}{'█' * filled_length}{Style.RESET_ALL}{'░' * (length - filled_length)}"


def _print_compliance_info(summary) -> None:
    """Print compliance rate and progress bar."""
    compliance_rate = _calculate_compliance_rate(summary)
    progress_bar = _create_progress_bar(compliance_rate)

    print(
        f"\n{Fore.BLUE}📊 Compliance Rate: {Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}{compliance_rate:.1f}%{Style.RESET_ALL}"
    )
    print(
        f"{Fore.BLUE}Progress: {Style.RESET_ALL}[{progress_bar}] {compliance_rate:.1f}%"
    )


def print_summary(summary, results):
    """Print a modern, visually appealing summary of the analysis results."""
    # Print header
    _print_table_header("📊 FONT ANALYSIS SUMMARY")

    # Print summary statistics
    _print_table_row("🔍 Found Fonts", str(len(summary.found_fonts)), Fore.BLUE)
    _print_table_row("✅ Allowed Fonts", str(len(summary.allowed_fonts)), Fore.GREEN)

    # Disallowed fonts with conditional styling
    disallowed_color = Fore.RED if len(summary.disallowed_fonts) > 0 else Fore.YELLOW
    disallowed_icon = "❌" if len(summary.disallowed_fonts) > 0 else "✅"
    _print_table_row(
        f"{disallowed_icon} Disallowed Fonts",
        str(len(summary.disallowed_fonts)),
        disallowed_color,
    )

    _print_table_row("📈 Total Analyzed", str(len(results)), Fore.MAGENTA)

    # Print status
    _print_status_row(summary)

    # Print footer
    _print_table_footer()

    # Display detailed font lists if there are results
    if len(results) > 0:
        _print_font_list(
            "Found Fonts", summary.found_fonts, Fore.WHITE, "🔍", "No fonts found"
        )

        _print_font_list(
            "Allowed Fonts", summary.allowed_fonts, Fore.GREEN, "✅", "No allowed fonts"
        )

        _print_font_list(
            "Disallowed Fonts",
            summary.disallowed_fonts,
            Fore.RED,
            "❌",
            "No disallowed fonts",
        )

        # Print compliance information
        _print_compliance_info(summary)
