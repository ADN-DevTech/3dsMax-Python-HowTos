import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threadprogressbar-autodesk",
    version="0.0.1",
    description="Update a progress bar from a thread",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=threadprogressbar:startup'},
    install_requires=[
        'qtpy'
    ],
    python_requires='>=3.7'
)
