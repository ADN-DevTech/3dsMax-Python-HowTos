import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyconsole-autodesk",
    version="0.0.1",
    description="pyconsole sample",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.autodesk.com/windish/maxpythontutorials",
    packages=setuptools.find_packages(),
    install_requires=[
        'jedi==0.17.2',
        'pyqtconsole'
    ],
    entry_points={'3dsMax': 'startup=pyconsole:startup'},
    python_requires='>=3.7'
)
