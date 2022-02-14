#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the lishogi.org lishoginet client.
# Copyright (C) 2016-2020 Niklas Fiekas <niklas.fiekas@backscattering.de>
# Copyright (C) 2022- TheYoBots (for lishogi) <contact@lishogi.org>
# See LICENSE.txt for licensing information.

import setuptools
import re
import os.path


with open(os.path.join(os.path.dirname(__file__), "lishoginet.py"), "rb") as f:
    # Trick: Strip imports of dependencies
    lishoginet = {}
    code = f.read().decode("utf-8")
    stripped_code = re.sub(r"^(\s*)(import requests\s*$)", r"\1pass", code, flags=re.MULTILINE).encode("utf-8")
    eval(compile(stripped_code, "lishoginet.py", "exec"), lishoginet)


def read_description():
    with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
        description = readme.read()

    return description


setuptools.setup(
    name="lishoginet",
    version=lishoginet["__version__"],
    author=lishoginet["__author__"],
    author_email=lishoginet["__email__"],
    description=lishoginet["__doc__"].replace("\n", " ").strip(),
    long_description=read_description(),
    long_description_content_type="text/x-rst",
    keywords="lishogi.org lishogi shogi stockfish usi",
    url="https://github.com/TheYoBots/lishoginet",
    py_modules=["lishoginet"],
    test_suite="test",
    install_requires=["requests>=2,<3"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Internet :: WWW/HTTP",
    ]
)