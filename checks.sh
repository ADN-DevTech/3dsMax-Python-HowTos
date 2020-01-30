#! /usr/bin/env bash
set -e
script=$(dirname $(readlink -f "$0"))
cd "$script"

lint() {
    for f in $(find "$script" -name "setup.py")
    do
        local package=$(basename $(dirname "$f"))
        echo "$package" 
        pylint "$script/$package/$package"
    done
}

checkmarkdowncodeblocks() {
    # find code blocks in markdown that don't specify the language
    git grep -n '```' -- "*.md" | 
        dos2unix | 
        awk 'NR % 2 == 1' | 
        grep '``` *$' | 
        sed "s/$/ code block does not specify language/g"

    # find references to max that are not 3ds Max
    git grep "[^a-zA-Z_]max[^a-zA-Z]" -- "*.py" "*.md" |
        sed "s/$/ uses max instead of 3ds Max/g"
}

lint
checkmarkdowncodeblocks
