# -*- coding: utf-8 -*-
import json
import os

from setuptools import setup

with open("setmeup/assets/assets.json", "r") as f:
    d = json.load(f)
assets = [os.sep.join(["assets", dir_, fn]) for dir_, fns in d.items() for fn in fns]
assets.append("assets/assets.json")

setup(
    name="setmeup",
    version="0.0.0",
    description="tools to help me set up a new computer",
    url="https://github.com/ericnchen/setmeup",
    author="Eric Chen",
    author_email="eric@ericnchen.com",
    license="MIT",
    packages=["setmeup"],
    python_requires=">=3.7, <4",
    install_requires=["click"],
    package_data={"setmeup": assets},
    include_package_data=True,
    entry_points={"console_scripts": ["setmeup = setmeup.cli:cli"]},
)
