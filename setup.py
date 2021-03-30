from os import path
from setuptools import setup, find_packages

# git checkout master
# git merge api_v2

setup(
    name="wsimple",
    version="2.1.0",
    author="Yusuf Ahmed",
    author_email="yusufahmed172@gmail.com",
    long_description=open("README.md").read(),
    packages=find_packages("src"),
    package_dir={"": "src"},
    description="Wsimple.py: a API and Web interface for Wealthsimple Trade",
    long_description_content_type="text/markdown",
    url="https://github.com/yusuf8ahmed/Wsimple",
    install_requires=[
        "loguru",
        "cloudscraper",
        "requests",
        "python-box",
        "websockets"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "images": ["*.svg"],
        "": ["*.md"]
    },
    platforms = 'any',
    keywords ='wsimple',
    python_requires='>=3',
    zip_safe = False
)