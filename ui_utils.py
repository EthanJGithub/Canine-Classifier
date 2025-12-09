"""
UI Utilities for Canine Classifier
Beautiful terminal colors, animations, and styling.
"""

import sys
import time

# ANSI Color Codes
class Colors:
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Reset
    RESET = '\033[0m'


# ASCII Art
DOG_LOGO = """
    / \\__
   (    @\\___
   /         O
  /   (_____/
 /_____/   U
"""

DOG_BANNER = f"""
{Colors.BRIGHT_YELLOW}     ╔═══════════════════════════════════════════════════════════╗
     ║                                                               ║
     ║  {Colors.BRIGHT_CYAN}██████╗ █████╗ ███╗   ██╗██╗███╗   ██╗███████╗{Colors.BRIGHT_YELLOW}            ║
     ║  {Colors.BRIGHT_CYAN}██╔════╝██╔══██╗████╗  ██║██║████╗  ██║██╔════╝{Colors.BRIGHT_YELLOW}            ║
     ║  {Colors.BRIGHT_CYAN}██║     ███████║██╔██╗ ██║██║██╔██╗ ██║█████╗{Colors.BRIGHT_YELLOW}              ║
     ║  {Colors.BRIGHT_CYAN}██║     ██╔══██║██║╚██╗██║██║██║╚██╗██║██╔══╝{Colors.BRIGHT_YELLOW}              ║
     ║  {Colors.BRIGHT_CYAN}╚██████╗██║  ██║██║ ╚████║██║██║ ╚████║███████╗{Colors.BRIGHT_YELLOW}            ║
     ║  {Colors.BRIGHT_CYAN} ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝╚══════╝{Colors.BRIGHT_YELLOW}            ║
     ║                                                               ║
     ║  {Colors.BRIGHT_WHITE}██████╗██╗      █████╗ ███████╗███████╗██╗███████╗██╗███████╗██████╗ {Colors.BRIGHT_YELLOW} ║
     ║  {Colors.BRIGHT_WHITE}██╔════╝██║     ██╔══██╗██╔════╝██╔════╝██║██╔════╝██║██╔════╝██╔══██╗{Colors.BRIGHT_YELLOW} ║
     ║  {Colors.BRIGHT_WHITE}██║     ██║     ███████║███████╗███████╗██║█████╗  ██║█████╗  ██████╔╝{Colors.BRIGHT_YELLOW} ║
     ║  {Colors.BRIGHT_WHITE}██║     ██║     ██╔══██║╚════██║╚════██║██║██╔══╝  ██║██╔══╝  ██╔══██╗{Colors.BRIGHT_YELLOW} ║
     ║  {Colors.BRIGHT_WHITE}╚██████╗███████╗██║  ██║███████║███████║██║██║     ██║███████╗██║  ██║{Colors.BRIGHT_YELLOW} ║
     ║  {Colors.BRIGHT_WHITE} ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝{Colors.BRIGHT_YELLOW} ║
     ║                                                               ║
     ╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

SIMPLE_BANNER = f"""
{Colors.BRIGHT_CYAN}╔══════════════════════════════════════════════════════════════════╗
║  {Colors.BRIGHT_YELLOW}🐕  {Colors.BOLD}{Colors.BRIGHT_WHITE}C A N I N E   C L A S S I F I E R{Colors.RESET}{Colors.BRIGHT_CYAN}  {Colors.BRIGHT_YELLOW}🐕{Colors.BRIGHT_CYAN}                    ║
║  {Colors.DIM}{Colors.WHITE}    Identify Your Dog's Breed with AI & Science{Colors.RESET}{Colors.BRIGHT_CYAN}                ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""


def clear_screen():
    """Clear the terminal screen."""
    print('\033[2J\033[H', end='')


def print_colored(text, color=Colors.WHITE, bold=False, end='\n'):
    """Print text with color."""
    style = Colors.BOLD if bold else ''
    print(f"{style}{color}{text}{Colors.RESET}", end=end)


def print_header(text, color=Colors.BRIGHT_CYAN):
    """Print a styled header."""
    width = 60
    padding = (width - len(text) - 2) // 2
    print(f"\n{color}{'═' * width}")
    print(f"║{' ' * padding}{Colors.BOLD}{Colors.BRIGHT_WHITE}{text}{Colors.RESET}{color}{' ' * (width - padding - len(text) - 2)}║")
    print(f"{'═' * width}{Colors.RESET}\n")


def print_subheader(text, color=Colors.BRIGHT_YELLOW):
    """Print a styled subheader."""
    print(f"\n{color}  ▸ {Colors.BOLD}{text}{Colors.RESET}")


def print_menu_option(number, text, icon="", color=Colors.BRIGHT_WHITE):
    """Print a styled menu option."""
    print(f"  {Colors.BRIGHT_CYAN}[{Colors.BRIGHT_YELLOW}{number}{Colors.BRIGHT_CYAN}]{Colors.RESET} {icon} {color}{text}{Colors.RESET}")


def print_success(text):
    """Print a success message."""
    print(f"\n  {Colors.BRIGHT_GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Print an error message."""
    print(f"\n  {Colors.BRIGHT_RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    """Print a warning message."""
    print(f"\n  {Colors.BRIGHT_YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text):
    """Print an info message."""
    print(f"  {Colors.BRIGHT_CYAN}ℹ {text}{Colors.RESET}")


def print_divider(char="─", width=60, color=Colors.DIM):
    """Print a divider line."""
    print(f"{color}{char * width}{Colors.RESET}")


def print_box(text, color=Colors.BRIGHT_CYAN, padding=2):
    """Print text in a box."""
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    width = max_width + padding * 2

    print(f"{color}╭{'─' * (width + 2)}╮{Colors.RESET}")
    for line in lines:
        pad_right = width - len(line)
        print(f"{color}│{Colors.RESET} {line}{' ' * pad_right} {color}│{Colors.RESET}")
    print(f"{color}╰{'─' * (width + 2)}╯{Colors.RESET}")


def loading_animation(text="Loading", duration=1.0, color=Colors.BRIGHT_CYAN):
    """Display a loading animation."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        print(f"\r{color}{frame} {text}...{Colors.RESET}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{' ' * (len(text) + 10)}\r", end='')  # Clear the line


def progress_bar(current, total, width=40, color=Colors.BRIGHT_GREEN):
    """Display a progress bar."""
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r  {color}[{bar}]{Colors.RESET} {Colors.BRIGHT_WHITE}{percent*100:.1f}%{Colors.RESET}", end='', flush=True)
    if current == total:
        print()


def confidence_bar(confidence, label="", width=30):
    """Display a confidence bar with color coding."""
    if confidence >= 80:
        color = Colors.BRIGHT_GREEN
    elif confidence >= 50:
        color = Colors.BRIGHT_YELLOW
    else:
        color = Colors.BRIGHT_RED

    filled = int(width * confidence / 100)
    bar = "█" * filled + "░" * (width - filled)

    print(f"  {Colors.BRIGHT_WHITE}{label:30}{Colors.RESET} {color}[{bar}] {confidence:.1f}%{Colors.RESET}")


def get_input(prompt, color=Colors.BRIGHT_CYAN):
    """Get styled user input."""
    return input(f"{color}  ▶ {Colors.BRIGHT_WHITE}{prompt}{Colors.RESET} ")


def get_choice(prompt, valid_choices, color=Colors.BRIGHT_CYAN):
    """Get a valid choice from user."""
    while True:
        choice = get_input(prompt, color).strip().lower()
        if choice in valid_choices:
            return choice
        print_error(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")


def confirm(prompt, default=True):
    """Get yes/no confirmation from user."""
    default_str = "[Y/n]" if default else "[y/N]"
    response = get_input(f"{prompt} {Colors.DIM}{default_str}{Colors.RESET}").strip().lower()

    if not response:
        return default
    return response in ['y', 'yes']


def print_result_card(title, items, color=Colors.BRIGHT_GREEN):
    """Print a result card with styled output."""
    print(f"\n{color}  ┌{'─' * 56}┐{Colors.RESET}")
    print(f"{color}  │  {Colors.BOLD}{Colors.BRIGHT_WHITE}{title:52}{Colors.RESET}{color}  │{Colors.RESET}")
    print(f"{color}  ├{'─' * 56}┤{Colors.RESET}")

    for item in items:
        if isinstance(item, tuple):
            label, value = item
            print(f"{color}  │{Colors.RESET}  {Colors.BRIGHT_WHITE}{label:25}{Colors.BRIGHT_YELLOW}{value:27}{Colors.RESET}{color}  │{Colors.RESET}")
        else:
            print(f"{color}  │{Colors.RESET}  {item:52}{color}  │{Colors.RESET}")

    print(f"{color}  └{'─' * 56}┘{Colors.RESET}")


def animate_text(text, delay=0.03, color=Colors.BRIGHT_WHITE):
    """Animate text appearing character by character."""
    for char in text:
        print(f"{color}{char}{Colors.RESET}", end='', flush=True)
        time.sleep(delay)
    print()


def print_breed_result(rank, breed, confidence):
    """Print a styled breed result."""
    # Medal icons for top 3
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    medal = medals.get(rank, "  ")

    # Color based on confidence
    if confidence >= 80:
        bar_color = Colors.BRIGHT_GREEN
    elif confidence >= 50:
        bar_color = Colors.BRIGHT_YELLOW
    else:
        bar_color = Colors.BRIGHT_RED

    # Build bar
    bar_width = 25
    filled = int(bar_width * confidence / 100)
    bar = "█" * filled + "░" * (bar_width - filled)

    print(f"  {medal} {Colors.BOLD}{Colors.BRIGHT_WHITE}{breed:28}{Colors.RESET} {bar_color}[{bar}]{Colors.RESET} {Colors.BRIGHT_WHITE}{confidence:5.1f}%{Colors.RESET}")
