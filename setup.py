import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clip",
    version="1.0.0",
    author="Erik Branger",
    description="clip: Cherenkov Light Intensity Prediction for nuclear safeguards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebranger/clip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        "scipy"
    ]

)