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

    while True:
        # Stores WPM and accuracy from the test
        wpm, accuracy = wpm_test(stdscr)

        stdscr.clear()
        stdscr.addstr("You have completed the test!")
        stdscr.addstr(f"\nYour WPM is {wpm}. Your accuracy is %{accuracy}.")
        stdscr.addstr("\nPress any key to try again.")
        stdscr.refresh()
        
        # Pressing any key restarts the WPM test
        key = stdscr.getch()

        # ESC key exits the program
        if key == 27:
            exit()

def start_screen(stdscr) -> None:
    """
    Displays the start screen.

    Args:
        stdscr: Object representing the standard terminal window.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to the speed typing test!")
    stdscr.addstr("\nPress any key to begin.")
    stdscr.addstr(curses.LINES - 1, 0, "Press ESC to exit the program at any time.")
    stdscr.refresh()

    # Pressing any key begins the program
    key = stdscr.getch()

    # ESC key exits the program
    if key == 27:
        exit()

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

    # Initializes WPM and accuracy
    wpm = 0
    accuracy = 100.0

    # Test runs until the length of input_chars matches length of target text
    while len(input_chars) < len(target):
        # Refreshes display
        stdscr.clear()
        accuracy = calculate_accuracy(target, input_chars)
        display_input(stdscr, target_lines, input_chars, width, accuracy)
        stdscr.refresh()

        # Retrieves user input characters
        try:
            key = stdscr.getch()
        except:
            continue

        # ESC key exits the program
        if key == 27:
            exit()
        # Backspace key deletes most recent character
        if key == 8:
            if len(input_chars) > 0:
                input_chars.pop()
        elif key == 530: # Handles single quote characters
            input_chars.append("'")
        elif key == 460: # Handles double quote characters
            input_chars.append("\"")
        else: # Adds most recent character to input_chars
            if len(input_chars) < len(target):
                input_chars.append(chr(key))

    return wpm, calculate_accuracy(target, input_chars)

def display_input(stdscr, target_lines: list, input_chars: list, width: int, 
                  accuracy:float = 100.0) -> None:
    """
    Displays target text along with user input.

    Args:
        stdscr: Object representing the standard terminal window.
        target_lines (list): List containing target text.
        input_chars (list): List containing user input characters.
        width (int): Width of the terminal window.
    """
    # Displays target text to the terminal
    for y, line in enumerate(target_lines):
        stdscr.addstr(y, 0, line)
    # Splits input into lines to fit the terminal window
    input_lines = textwrap.fill("".join(input_chars), width).splitlines()

    stdscr.addstr(len(target_lines) + 2, 0, f"Accuracy: %{accuracy}")

    # Writes user input to the terminal
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if y < len(target_lines) and x < len(target_lines[y]):
                target_char = target_lines[y][x]
                # Sets text colour to green if character matches target text, red otherwise
                text_colour = curses.color_pair(1) if char == target_char else curses.color_pair(2)
                stdscr.addstr(y, x, target_char, text_colour)

def calculate_accuracy(target: str, input_chars: list) -> float:
    """
    Calculates the accuracy at the current time.

    Args:
        target (str): String containing target text.
        input_chars (list): List containing user input characters.

    Returns:
        float: A float containing the calculated accuracy rounded to one decimal point.
    """
    # Returns 100 if input_chars is empty
    if len(input_chars) == 0:
        return 100.0
    else:
        # Calculates number of matching characters
        matching_chars = 0
        for i in range(len(input_chars)):
            if input_chars[i] == target[i]:
                matching_chars += 1
        # Divides matching characters by total length of the input
        return round((matching_chars / len(input_chars)) * 100, 1)

curses.wrapper(main)