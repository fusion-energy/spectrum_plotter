import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spectrum_plotter",
    version="develop",
    author="The Spectrum Plotter Development Team",
    author_email="mail@jshimwell.com",
    description="A Python package for creating publication quality plots for neutron / photon / particle spectrum ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/spectrum_plotter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        "spectrum_plotter": [
            # "requirements.txt",
            "README.md",
            "LICENSE",
        ]
    },
    install_requires=[
        'numpy>=1.9',
        "matplotlib>=3.2.2",
        "plotly",
        "openmc_post_processor",
        # "kaleido"  # required to save static images with plotly
    ],
)
