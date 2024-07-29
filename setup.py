import os
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="codeshuttle",
    version="0.1.0",  # Update this as you release new versions
    author="Anton Sakharov",
    author_email="qlmmlp@gmail.com",
    description="A tool to streamline code transfers between AI assistants and source files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qlmmlp/codeshuttle",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'codeshuttle=codeshuttle.codeshuttle:main',
        ],
    },
    include_package_data=True,
    package_data={
        'codeshuttle': ['py.typed'],
    },
)