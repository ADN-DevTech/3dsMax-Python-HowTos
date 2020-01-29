#! /usr/bin/env bash
set -e
script=$(dirname $(readlink -f "$0"))

lint() {
    for f in $(find "$script" -name "setup.py")
    do
        local package=$(basename $(dirname "$f"))
        echo "$package" 
        pylint "$script/$package/$package"
    done
}

lint
