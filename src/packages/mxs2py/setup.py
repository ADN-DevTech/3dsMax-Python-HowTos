import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxs2py-autodesk",
    version="0.0.1",
    description="mxs2py converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ADN-DevTech/3dsMax-Python-HowTos",
    packages=setuptools.find_packages(),
    install_requires = [
        'parsec==3.12'
        ],
    python_requires='>=3.7'
)
