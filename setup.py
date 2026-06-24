from setuptools import setup, find_packages

setup(
    name="angel-in-pocket",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiogram>=3.0.0",
        "pyyaml>=6.0",
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.9",
)
