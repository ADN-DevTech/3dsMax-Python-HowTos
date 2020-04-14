#! /usr/bin/env bash
set -e
# create the Splash.png preview
montage -size 400x400 **/**/*.png -thumbnail 300x300 +polaroid -resize 50% -gravity center -background none -extent 180x180 -background White -geometry -10+2  -tile x1  Splash.png
echo "Done"
