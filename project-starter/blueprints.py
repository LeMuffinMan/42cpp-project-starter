
import os
from utils import SRC_DIR, INC_DIR, generate_guard

def write_main():
    main_path = os.path.join(SRC_DIR, "main.cpp")
    if os.path.exists(main_path):
        return False, "main.cpp already exists. Generation aborted."
    main_content = """int main(void)
{
    return 0;
}
"""
    with open(main_path, "w") as f:
        f.write(main_content)
    return True, "main.cpp generated."


def write_makefile(NAME):
    makefile_path = "Makefile"

    if os.path.exists(makefile_path):
        return False
        "Makefile already exists. Generation aborted."

    src_files = [os.path.join(SRC_DIR, f) for f in os.listdir(SRC_DIR) if f.endswith(".cpp")]
    src_list = " ".join(src_files)

    makefile_content = f"""CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++98 -I{INC_DIR}
SRC = {src_list}
OBJ = $(SRC:.cpp=.o)
NAME = {NAME}

all: $(NAME)

$(NAME): $(OBJ)
\t$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
\t$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
\trm -f $(OBJ) $(NAME)

.PHONY: all clean
"""
    with open(makefile_path, "w") as f:
        f.write(makefile_content)
    return True, "Makefile generated."


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

