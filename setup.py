# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name="hackathon",
    version="0.0.1",
    description="hackathon team 15",
    long_description=readme,
    author="TEAM15",
    author_email="hugo.vasquez10@gmail.com",
    url="https://github.com/HugoVazquez-x/MistralAI-Game-Jam-Team-15",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)