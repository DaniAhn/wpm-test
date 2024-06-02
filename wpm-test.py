import curses
import textwrap
import time

def main(stdscr) -> None:
    """
    Main entry point of the program.

    Args:
        stdscr: Object representing the standard terminal window.
    """
    # Sets custom text background colour
    curses.init_color(10, 300, 300, 300)

    # Sets custom text colour pairs
    curses.init_pair(1, curses.COLOR_GREEN, 10)
    curses.init_pair(2, curses.COLOR_RED, 10)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)

def start_screen(stdscr) -> None:
    """
    Displays the start screen.

    Args:
        stdscr: Object representing the standard terminal window.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to the speed typing test!")
    stdscr.addstr("\nPress any key to begin typing.")
    stdscr.refresh()
    stdscr.getkey()

def wpm_test(stdscr) -> None:
    """
    Runs the WPM test.

    Args:
        stdscr: Object representing the standard terminal window.
    """
    # Target string for the typing test
    target = ("Words per minute (WPM) is a measure of typing speed, commonly"
              " used in recruitment. For the purposes of WPM measurement a "
              "word is standardized to five characters or keystrokes. "
              "Therefore, \"brown\" counts as one word, but \"accounted\" "
              "counts as two. The benefits of a standardized measurement of "
              "input speed are that it enables comparison across language "
              "and hardware boundaries. The speed of an Afrikaans-speaking "
              "operator in Cape Town can be compared with a French-speaking "
              "operator in Paris. (Wikipedia)")
    # List containing user input characters
    input_chars = []

    # Splits target string into lines to fit the terminal window
    height, width = stdscr.getmaxyx()
    target_lines = textwrap.fill(target, width).splitlines()

    while True:
        # Refreshes display
        stdscr.clear()
        display_input(stdscr, target_lines, input_chars, height, width)
        stdscr.refresh()

        # Retrieves user input characters
        key = stdscr.getch()

        # ESC key exits the program
        if key == 27:
            break
        # Backspace key deletes most recent character
        if key == 8:
            if len(input_chars) > 0:
                input_chars.pop()
        elif key == 530: # Handles single quote characters
            input_chars.append("'")
        elif key == 460: # Handles double quote characters
            input_chars.append("\"")
        else: # Adds most recent character to input_chars
            input_chars.append(chr(key))

def display_input(stdscr, target_lines: list, input_chars: list, height: int, width: int) -> None:
    """
    Displays target text along with user input.

    Args:
        stdscr: Object representing the standard terminal window.
        target_lines (list): List containing target text.
        input_chars (list): List containing user input characters.
        height (int): Height of the terminal window.
        width (int): Width of the terminal window.
    """
    # Displays target text to the terminal
    for y, line in enumerate(target_lines):
        stdscr.addstr(y, 0, line)
    # Splits input into lines to fit the terminal window
    input_lines = textwrap.fill("".join(input_chars), width).splitlines()

    # Writes user input to the terminal
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if y < len(target_lines) and x < len(target_lines[y]):
                target_char = target_lines[y][x]
                # Sets text colour to green if character matches target text, red otherwise
                text_colour = curses.color_pair(1) if char == target_char else curses.color_pair(2)
                stdscr.addstr(y, x, target_char, text_colour)

curses.wrapper(main)