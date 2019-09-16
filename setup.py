import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aul",
    version="0.1",
    author="Patrick Steinmann",
    author_email="patrick.steinmann@wur.nl",
    description="A package to export NetLogo simulation runs in GIF or MP4 formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steipatr/aul",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)