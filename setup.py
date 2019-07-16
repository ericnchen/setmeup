# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name="dtf",
    version="0.1.2",
    description="dtf is my personal dotfile manager.",
    url="https://github.com/ericnchen/dtf",
    author="Eric Chen",
    author_email="eric@ericnchen.com",
    license="MIT",
    packages=["dtf", "dtf.dotfiles"],
    python_requires=">=3.7, <4",
    install_requires=["click"],
    include_package_data=True,
    entry_points={"console_scripts": ["dtf = dtf.app:cli"]},
)
