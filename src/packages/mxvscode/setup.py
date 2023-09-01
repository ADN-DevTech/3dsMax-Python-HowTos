import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxvscode-autodesk",
    version="0.0.1",
    description="Let the VS Code debugger attach to 3ds Max",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'debugpy'
    ],
    entry_points={'3dsMax': 'startup=mxvscode:startup'},
    python_requires='>=3.7'
)
