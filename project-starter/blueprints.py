
import os
from utils import SRC_DIR, INC_DIR, generate_guard

def write_main():
    main_path = os.path.join(SRC_DIR, "main.cpp")
    if os.path.exists(main_path):
        return False, "main.cpp already exists. Generation aborted."
    
    class_includes = []
    if os.path.exists(INC_DIR):
        for file in os.listdir(INC_DIR):
            if file.endswith(".hpp"):
                class_name = file[:-4]  # Enlève l'extension .hpp
                class_includes.append(f'#include "{file}"')
    
    includes_content = "\n".join(class_includes) + "\n\n" if class_includes else ""
    
    main_content = f"""{includes_content}int main(void)
{{
    return 0;
}}
"""
    with open(main_path, "w") as f:
        f.write(main_content)
    return True, "main.cpp generated with class includes."


def write_makefile(NAME):
    makefile_path = "Makefile"
    message = ""

    if os.path.exists(makefile_path):
        backup_path = "Makefile.bak"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        shutil.move(makefile_path, backup_path)
        message = f"Old Makefile backed up as {backup_path}"

    src_files = [os.path.join(SRC_DIR, f) for f in os.listdir(SRC_DIR) if f.endswith(".cpp")]
    src_list = " ".join(src_files)

    makefile_content = f"""CXX = c++
CXXFLAGS = -Wall -Wextra -Werror -std=c++98 -I{INC_DIR} -MMD -MP
SRC_DIR = src
OBJS_DIR = .objs
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJS_DIR)/%.o,$(SRCS))
DEPS = $(OBJS:.o=.d)

NAME = {NAME}

all: $(NAME)

$(NAME): $(OBJS) 
\t$(CXX) $(CXXFLAGS) -o $@ $^

$(OBJS_DIR)/%.o: $(SRC_DIR)/%.cpp Makefile | $(OBJS_DIR)
\t$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJS_DIR):
\tmkdir -p $(OBJS_DIR)

-include $(DEPS)

clean:
\trm -rf $(OBJS_DIR)

fclean: clean
\trm -f $(NAME)

re: fclean all

run: all 
\t./$(NAME)

vg: 
\t$(VG) $(VGFLAGS) ./$(NAME) 

.PHONY: all clean fclean re run vg"""

    with open(makefile_path, "w") as f:
        f.write(makefile_content)
    # Return both the success status and the message
    return True, message or "Makefile generated."  # This will return either the backup message or the default success message


def write_class_files(class_name):
    hpp_path = os.path.join(INC_DIR, f"{class_name}.hpp")
    cpp_path = os.path.join(SRC_DIR, f"{class_name}.cpp")

    if os.path.exists(hpp_path) or os.path.exists(cpp_path):
        return False, f"Error : {hpp_path} or {cpp_path} already exists."

    guard = generate_guard(class_name)
    hpp_content = f"""#ifndef {guard}
#define {guard}

class {class_name}
{{
public:
    {class_name}(); // Default constructor
    {class_name}(const {class_name}& other); // Copy constructor
    {class_name}& operator=(const {class_name}& other); // Copy assignment
    ~{class_name}(); // Destructor

private:
    // Add private members here
}};

#endif
"""

    cpp_content = f"""#include "{class_name}.hpp"
#include <iostream>

{class_name}::{class_name}()
{{
    std::cout << "{class_name} Default constructor called" << std::endl;
}}

{class_name}::{class_name}(const {class_name}& other)
{{
    std::cout << "{class_name} Copy constructor called" << std::endl;
}}

{class_name}& {class_name}::operator=(const {class_name}& other)
{{
    std::cout << "{class_name} Copy assignment operator called" << std::endl;
    if (this != &other) {{
        // complete here
    }}
    return *this;
}}

{class_name}::~{class_name}()
{{
    std::cout << "{class_name} Destructor called" << std::endl;
}}

// Here write any other utility functions for this class
"""
    with open(hpp_path, "w") as f:
        f.write(hpp_content)
    with open(cpp_path, "w") as f:
        f.write(cpp_content)

    return True, f"Classe {class_name} generated."

