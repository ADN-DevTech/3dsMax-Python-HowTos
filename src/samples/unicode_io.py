"""
    Demonstrate file io using unicode paths and unicode content.
"""
import tempfile
import os
import codecs
import shutil

# Strings for the file content
TEXT_STR = 'Text String: Hello!\n'
UNI_TEXT_STR = 'Unicode String: 女時代'

# Get the current working folder
CURRENT_DIR = os.getcwd()

# Create Unicode directory name
UNI_DIR = '時'

# Set our user folder to the user temp folder
TEMP_DIR = tempfile.gettempdir()

# Create Unicode file name
UNI_FILE = 'Pÿ x Mxs.txt'

# Set our temp folder plus the Unicode directory
FULL_PATH = TEMP_DIR + '\\' + UNI_DIR

# Set our filename
F_NAME = UNI_FILE

def create_uni_dir():
    """Create a directory with a unicode name."""
    # Remove directory if it already exists
    if os.path.exists(FULL_PATH):
        remove_uni_dir()
    try:
        # Make sure we are in the correct directory root
        os.chdir(TEMP_DIR)
        print('Working Directory:\n ' + os.getcwd())
    except IOError:
        print('!FAIL! Could not set working directory!\n')
    else:
        print('Moved to Temp folder:\n ' + os.getcwd())

    try:
        # Make our directory
        os.mkdir(FULL_PATH)
    except IOError:
        print('FAIL! Could not create unicode directory:\n' + FULL_PATH)
    else:
        print('Created unicode directory:\n' + FULL_PATH)

def remove_uni_dir():
    """Remove a directory with a unicode name."""
    # Check if the directory exists
    if os.path.exists(FULL_PATH):
        try:
            # Change to our working folder to be safe
            os.chdir(TEMP_DIR)
            print('Working Directory:\n ' + os.getcwd())
        except IOError:
            print('!FAIL! Directory does not exist!\n')
        else:
            # Since we know we are in our working folder, remove the Unicode
            # directory created my createDir()
            shutil.rmtree(UNI_DIR)
            print('Removed unicode directory:\n' + FULL_PATH)

def open_file():
    """Open a file in working directory and write in it."""
    # Change to our working folder to be safe
    os.chdir(TEMP_DIR)
    # Set up our file and set it's encoding to UTF-8
    with codecs.open(F_NAME, encoding='utf-8', mode='w+') as thefile:
        # Write to our file (this could be done as a try)
        thefile.write(TEXT_STR + UNI_TEXT_STR)
        print('Finished writing file to ' + F_NAME)
        # Close our file
        thefile.close()

def open_file_in_uni_dir():
    """Open a file in unicode directory and write in it."""
    # Change to our working folder to be safe
    os.chdir(FULL_PATH)
    # Set up our file and set it's encoding to UTF-8
    with codecs.open(F_NAME, encoding='utf-8', mode='w+') as thefile:
        # Write to our file (this could be done as a try)
        thefile.write(TEXT_STR + UNI_TEXT_STR)
        print('Finished writing file to ' + FULL_PATH + F_NAME)
        # Close our file
        thefile.close()

def remove_uni_file():
    """Remove a unicode file."""
    # Change to our working folder to be safe
    os.chdir(TEMP_DIR)
    # Check if the file exists
    if os.path.exists(TEMP_DIR + F_NAME):
        print('File ' + F_NAME + ' exists and will be removed!')
        try:
            # Remove our file
            os.remove(TEMP_DIR + F_NAME)
        except IOError:
            print('!FAIL! - File not deleted')
        else:
            print('File Removed.')

# Create some setup stats for output
try:
    STATS = unicode(
        'Setup:\n' +
        'Current directory: ' +
        CURRENT_DIR +
        '\nOutput filename: ' +
        UNI_FILE +
        '\nFile contents: ' +
        TEXT_STR +
        UNI_TEXT_STR)
except NameError:
    STATS = (
        'Setup:\n' +
        'Current directory: ' +
        CURRENT_DIR +
        '\nOutput filename: ' +
        UNI_FILE +
        '\nFile contents: ' +
        TEXT_STR +
        UNI_TEXT_STR)
# Output stats
print(STATS)

# Run our functions
open_file()
create_uni_dir()
open_file_in_uni_dir()
# Comment these out to leave written files and created directory
# to visually verify files and files content
remove_uni_dir()
remove_uni_file()
