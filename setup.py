from setuptools import setup, find_packages
import os

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

branch = os.getenv('GITHUB_REF', 'master').split('/')[-1]  # Default to 'master' if GITHUB_REF is not set
url = f"https://github.com/armurox/loggingredactor/tree/{branch}"

# Get version from environment variable
version = os.getenv('RELEASE_VERSION', '0.0.1')  # Default to '0.0.1' if RELEASE_VERSION is not set
# Get development status
split_version = version.split('-')
if len(split_version) == 2:
    release_mode = split_version[1][0].upper()
    status = split_version[1][-1] + ' - ' + release_mode
    status += 'lpha' if release_mode == 'A' else 'eta'
else:
    status = 'Production'

setup(
    name="loggingredactor",
    packages=find_packages(),
    version=version,
    url=url,
    description="Redact data in logs based on regex filters and keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arman Jasuja",
    author_email="arman_jasuja@yahoo.com",
    classifiers=[
        f"Development Status :: {status}",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.7',
)
