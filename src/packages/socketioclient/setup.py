import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="socketioclient-autodesk",
    version="0.0.1",
    description="socketioclient sample",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.autodesk.com/windish/maxpythontutorials",
    packages=setuptools.find_packages(),
    install_requires=[
        'python-socketio',
        'websocket-client'
    ],
    python_requires='>=3.7'
)
