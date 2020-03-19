import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickpreview-autodesk",
    version="0.0.1",
    description="Create a quick preview",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=quickpreview:startup'},
    python_requires='>=3.7'
)
