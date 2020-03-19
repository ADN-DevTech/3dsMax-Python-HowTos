import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zdepthchannel-autodesk",
    version="0.0.1",
    description="Access the Z-Depth Channel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=zdepthchannel:startup'},
    python_requires='>=3.7'
)
