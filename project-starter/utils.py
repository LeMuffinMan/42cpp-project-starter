
import os

SRC_DIR = "src"
INC_DIR = "include"

def ensure_dirs():
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    if not os.path.isdir(INC_DIR):
        os.makedirs(INC_DIR)

# we need to format text for #ifndef 
def generate_guard(class_name):
    guard = f"{class_name}_HPP".upper()
    guard = "".join(c if c.isalnum() or c == '_' else '_' for c in guard).rstrip('_')
    return guard


