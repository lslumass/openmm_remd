from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="openmm_remd",
    version="0.1.0",
    author="Shanlong Li",
    author_email="shanlongli@umass.edu",
    description="the remd part of cg_openmm package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lslumass/opemm_remd",
    packages=["openmm_remd"],
    package_dir={"openmm_remd": "rep_exch"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib>=3.1.0",
        "numpy>=1.17.0",
    ],
)
