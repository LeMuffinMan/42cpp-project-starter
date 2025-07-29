
import os
import curses

def main(stdscr):
    global NAME

    curses.curs_set(0)
    new_sources = False;
    del_sources = False;

    if not os.path.exists("Makefile"):
        return False
        "No Makefile found. Generate a Makefile now ?"
        #recuperer une entree y / n
        #appeler write_makefile si oui
        # si non on exit

    while True:
        stdscr.clear()
        stdscr.addstr(f"Makefile to update : \n")
        #afficher le chemin vers le Makefile repere
        stdscr.addstr(f"Sources found in src folder :\n")
        #afficher une liste des .cpp dispos dans src
        stdscr.addstr(f"Sources found in Makefile :\n")
        #affiche une liste des .cpp trouve dans le Makefile
        stdscr.addstr(f"A) Update Makefile with following new sources : {'Yes' if new_sources else 'No'}\n")
        #afficher les srcs de src pas presente dans Makefile
        stdscr.addstr(f"D) Update Makefile deleting following sources : {'Yes' if del_sources else 'No'}\n")
        #afficher les srcs de Makefile qui ne sont pas dans src
        stdscr.addstr(f"B) Generate a backup \".bk\" : {'Yes' if backup else 'No'}\n")
        stdscr.addstr(f"U) Update Makefile and quit")
        stdscr.addstr(f"Q) Quit without update Makefile")
        
        c = stdscr.getch()

        if c == ord('A'):
            new_sources = not new_sources
        elif c == ord('D'):
            del_sources = not del_sources
        elif c == ord('B'):
            backup = not backup
        elif c == ord('U'):
            #update
            stdscr.addstr("Updateing Makefile")
            break 
        elif c == ord('Q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
