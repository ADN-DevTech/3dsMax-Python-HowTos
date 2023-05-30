import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxstranslate-autodesk",
    version="0.0.1",
    description="Translation window for mxs code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.autodesk.com/windish/maxpythontutorials",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=mxstranslate:startup'},
    install_requires=[
        'pygments'
    ],    
    python_requires='>=3.7'
)
