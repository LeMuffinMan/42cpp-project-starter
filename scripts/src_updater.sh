
#!/bin/bash

MAKEFILE="Makefile"

if [ ! -f "$MAKEFILE" ]; then
    echo "Error: $MAKEFILE not found in the current directory."
    exit 1
fi

read -p "Generate a backup of the existing Makefile before update ? (y/n): " backup_choice
if [[ "$backup_choice" =~ ^[Yy]$ ]]; then
    cp "$MAKEFILE" "$MAKEFILE.bak"
    echo "Backup created: $MAKEFILE.bak"
fi

files=$(find src/ -type f -name '*.cpp' | sort)

if [ -z "$files" ]; then
    echo "No source files found in src/"
    exit 1
fi

new_src_line="SRCS ="
for f in $files; do
    new_src_line+=" $f"
done

sed -i -E "s|^SRCS\s*=.*|$new_src_line|" "$MAKEFILE"

echo "Makefile updated:"
echo "$new_src_line"

