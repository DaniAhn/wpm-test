import curses
import textwrap
import time

def main(stdscr) -> None:
    """
    Main entry point of the program.

    Args:
        stdscr: Object representing the standard terminal window.
    """
    # Sets custom text colour pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Sets cursor to be invisible
    curses.curs_set(0)

    start_screen(stdscr)

    while True:
        # Stores WPM and accuracy from the test
        wpm, accuracy = wpm_test(stdscr)

        stdscr.clear()
        stdscr.addstr("You have completed the test!")
        stdscr.addstr(f"\nYour WPM is {wpm}. Your accuracy is {accuracy}%.")
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

    # Ensures loop runs in real time
    stdscr.nodelay(True)
    start_time = time.time()

    while True:
        # Calculates WPM and accuracy
        wpm = calculate_wpm(start_time, input_chars)
        accuracy = calculate_accuracy(target, input_chars)

        # Refreshes display
        stdscr.clear()
        display_input(stdscr, target_lines, input_chars, width, accuracy, wpm)
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
        else: 
            try:
                if key == 530: # Handles single quote characters
                    if len(input_chars) < len(target):
                        input_chars.append("'")
                elif key == 460: # Handles double quote characters
                    if len(input_chars) < len(target):
                        input_chars.append("\"")
                elif key == 32:  # Handles space character
                    if len(input_chars) < len(target):
                        input_chars.append(" ")
                else: # Adds most recent character to input_chars
                    if len(input_chars) < len(target):
                        input_chars.append(chr(key))
            except ValueError:
                pass
        
        # Test runs until the length of input matches length of target text
        if len(input_chars) >= len(target):
            break
    
    stdscr.nodelay(False)

    return calculate_wpm(start_time, input_chars), calculate_accuracy(target, input_chars)

def display_input(stdscr, target_lines: list, input_chars: list, width: int, 
                  accuracy: float = 100.0, wpm: int = 0) -> None:
    """
    Displays target text along with user input.

    Args:
        stdscr: Object representing the standard terminal window.
        target_lines (list[str]): List containing target text.
        input_chars (list[str]): List containing user input characters.
        width (int): Width of the terminal window.
    """
    # Displays target text to the terminal
    for y, line in enumerate(target_lines):
        stdscr.addstr(y, 0, line)
    # Splits input into lines to fit the terminal window
    input_lines = textwrap.fill("".join(input_chars), width).splitlines()

    # Updates and displays WPM and accuracy
    stdscr.addstr(len(target_lines), 0, f"WPM: {wpm}")
    stdscr.addstr(len(target_lines) + 1, 0, f"Accuracy: {accuracy}%")

    # Writes user input to the terminal
    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if y < len(target_lines) and x < len(target_lines[y]):
                target_char = target_lines[y][x]
                # Sets text colour to green if character matches target text, red otherwise
                if char == target_char:
                    text_colour = curses.color_pair(1)
                else:
                    text_colour = curses.color_pair(2)
                
                stdscr.addstr(y, x, target_char, text_colour)

def calculate_accuracy(target: str, input_chars: list) -> float:
    """
    Calculates the accuracy at the current time.

    Args:
        target (str): String containing target text.
        input_chars (list[str]): List containing user input characters.

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
    
def calculate_wpm(start_time: float, input_chars: list) -> int:
    """
    Calculates the WPM at the current time.

    Args:
        start_time (float): The starting time to measure from.
        input_chars (list[str]): List containing user input characters.

    Returns:
        int: An integer containing the current WPM.
    """
    # Calculates how much time has passed since the starting time
    elapsed_time = time.time() - start_time

    # elapsed_time is set to 1 to prevent a zero division error
    if elapsed_time < 1:
        elapsed_time = 1

    # Performs the WPM calculation
    return int((len(input_chars) / (elapsed_time / 60)) / 5)

curses.wrapper(main)