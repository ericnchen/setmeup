# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name="setmeup",
    version="0.1.0",
    description="tools to help me set up a new computer",
    url="https://github.com/ericnchen/setmeup",
    author="Eric Chen",
    author_email="eric@ericnchen.com",
    license="MIT",
    packages=["setmeup", "setmeup.dotfiles"],
    python_requires=">=3.7, <4",
    install_requires=["click"],
    include_package_data=True,
    entry_points={"console_scripts": ["dtf = setmeup.cli:main"]},
)
