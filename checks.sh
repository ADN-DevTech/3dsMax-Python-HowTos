#! /usr/bin/env bash
set -e
script=$(dirname $(readlink -f "$0"))
workdir=$(pwd)
IFS=$'\n'

lint() {
    for f in $(find . -name "setup.py")
    do
        local package=$(basename $(dirname "$f"))
        echo "$package" 
        pylint "./$package/$package"
        # also prevent runtime.execute
        if grep -n -R -E "runtime\.execute\(|rt.execute\(" --include '*.py' "./$package/$package"
        then 
            echo "pymxs.execute used"
            exit 1
        fi
    done
}

checkmarkdown() {
    # find code blocks in markdown that don't specify the language
    git grep -n '```' -- "*.md" | 
        dos2unix | 
        awk 'NR % 2 == 1' | 
        grep '``` *$' | 
        sed "s/$/ code block does not specify language/g"

    # find references to max that are not 3ds Max
    git grep "[^a-zA-Z_]max[^a-zA-Z]" -- "*.py" "*.md" |
        sed "s/$/ uses max instead of 3ds Max/g"
    git grep -n "[^a-zA-Z_\`.]python[^a-zA-Z_]" -- "*.md" | 
        sed "s/$/: python should be spelled Python/g"
}

checkmdlinks() {
    file=$1
    filedir=$(dirname "$file")
    # iterate all links in the file
    for link in $(grep -n -o "\[[^]]*\]([^)]*)" "$file")
    do
        url=$(echo "$link" | sed -e "s/^[^:]*://" -e "s/\[[^]]*\]//" -e "s/^(//" -e "s/)$//")
        line=$(echo "$link" | grep -o "^[^:]*")
        if [[ "$url" =~ ^https?:.* ]]
        then
            if ! curl --output /dev/null --silent --head "$url"
            then
                echo "$file:$line: Broken url (no head): $url"
            fi
        elif [[ "$url" =~ ^/.* ]]
        then
            if [ ! -f "$workdir$url" ]
            then
                echo "$file$line: Broken absolute link: $url"
            fi
        else
            if [ ! -f "$filedir/$url" ]
            then
                echo "$file:$line: Broken relative link: $url"
            fi
        fi
    done
}

checkmarkdownlinks() {
    # iterate all matching markdown files in the repo
    for f in $(git grep --name-only "\[[^]]*\]([^)]*)" -- "*.md")
    do
        checkmdlinks "$f"
    done
}


lint
checkmarkdown
checkmarkdownlinks
