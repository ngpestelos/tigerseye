#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name = 'Tigerseye',
  version = '0.1',
  description = 'Processing feed URLs',
  long_description = """Import and manipulate feed URLs""",
  author = 'Nestor G Pestelos Jr',
  author_email = 'ngpestelos@gmail.com',
  license = 'BSD',
  url = '',
  zip_safe = True,
  classifiers = [
      'Development Status :: 3 - Alpha'],
  packages = ['tigerseye'],
  test_suite = '',
  install_requires = []
)
