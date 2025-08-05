
import curses
from blueprints import write_class_files, write_main, write_makefile
from utils import ensure_dirs

def prompt_string(stdscr, prompt):
    stdscr.addstr(prompt)
    stdscr.refresh()
    curses.echo()
    s = stdscr.getstr().decode()
    curses.noecho()
    return s.strip()

def main(stdscr):
    global NAME  # pour modifier la variable globale

    curses.curs_set(0)
    ensure_dirs()

    classes = []
    option_main = False
    option_makefile = False

    while True:
        # This is the text displayed on the TUI
        stdscr.clear()
        stdscr.addstr("=== C++ project generator ===\n\n")
        stdscr.addstr("A) Add a class\n")
        stdscr.addstr("m) Generate main.cpp\n")
        stdscr.addstr("M) Generate Makefile\n")
        stdscr.addstr("\n")
        if classes:
            class_list_str = "\n - " + "\n - ".join(classes)
        else:
            class_list_str = "(none)"
        stdscr.addstr(f"Classes to create :{class_list_str}\n")
        stdscr.addstr(f"Create main.cpp : {'Yes' if option_main else 'No'}\n")
        stdscr.addstr(f"Create Makefile : {'Yes' if option_makefile else 'No'}\n\n")
        if option_makefile and NAME:
            stdscr.addstr(f"Name: {NAME}\n")
        stdscr.addstr("\n")
        stdscr.addstr("G) Generate and quit\n")
        stdscr.addstr("Q) Quit without generation\n\n")
        stdscr.refresh()

        #This allow to get the next user input
        c = stdscr.getch()

        # switch case for each command
        if c == ord('A') or c == ord('a'):
            stdscr.clear() #we need another screen for class creation
            class_name = prompt_string(stdscr, "Class name (empty to cancel) : ")
            #copy the str input in classes tab
            if class_name:
                classes.append(class_name)
        #switches on / off 
        elif c == ord('m'):
            option_main = not option_main
        elif c == ord('M'):
            if option_makefile == False:
                stdscr.clear()
                NAME = prompt_string(stdscr, "Binary name : ")
            option_makefile = not option_makefile
        # execute the generation 
        elif c == ord('G') or c == ord('g'):
            stdscr.clear()
            # we need a new screen for debug info
            stdscr.refresh()
            messages = []
            for cl in classes:
                success, msg = write_class_files(cl)
                #we store the exit code for debug infos
                messages.append(msg)
            if option_main:
                success, msg = write_main()
                messages.append(msg)
            if option_makefile:
                success, msg = write_makefile(NAME)
                messages.append(msg)
            # print all debug infos
            stdscr.addstr("\n".join(messages) + "\n\n")
            stdscr.addstr("Press any key to quit.")
            stdscr.refresh()
            stdscr.getch()
            break
        elif c == ord('Q') or c == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)


