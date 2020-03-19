import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="removeallmaterials-autodesk",
    version="0.0.1",
    description="A sample 3ds Max Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=removeallmaterials:startup'},
    python_requires='>=3.7'
)
