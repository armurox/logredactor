from setuptools import setup, find_packages

try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="loggingredactor",
    packages=find_packages(),
    version="0.0.1",
    url="https://github.com/armurox/loggingredacto",
    description="Redact logs based on regex filters and keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
