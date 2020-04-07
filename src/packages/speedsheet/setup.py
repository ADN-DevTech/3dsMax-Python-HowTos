import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speedsheet-autodesk",
    version="0.0.1",
    description="Output Object Data to File",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=speedsheet:startup'},
    python_requires='>=3.7'
)
