#!/bin/bash

TARGET_DIR="${1:-.}"  # Prend le répertoire courant par défaut
MAKEFILE="$TARGET_DIR/Makefile"

if [ ! -f "$MAKEFILE" ]; then
    echo "Error: $MAKEFILE not found in $TARGET_DIR"
    exit 1
fi

read -p "Generate a backup of the existing Makefile before update? (y/n): " backup_choice
if [[ "$backup_choice" =~ ^[Yy]$ ]]; then
    cp "$MAKEFILE" "$MAKEFILE.bak"
    echo "Backup created: $MAKEFILE.bak"
fi

# On cherche les fichiers depuis le répertoire cible
files=$(find "$TARGET_DIR/src/" -type f -name '*.cpp' | sort | sed "s|^$TARGET_DIR/||")

if [ -z "$files" ]; then
    echo "No source files found in $TARGET_DIR/src/"
    exit 1
fi

new_src_line="SRCS ="
for f in $files; do
    new_src_line+=" $f"
done

sed -i -E "s|^SRCS\s*=.*|$new_src_line|" "$MAKEFILE"
sed -i -E "s|^SRCS\s*[:]?=.*|$new_src_line|" "$MAKEFILE"

echo "Makefile in $TARGET_DIR updated:"
echo "$new_src_line"
