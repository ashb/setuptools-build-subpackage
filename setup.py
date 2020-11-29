#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from os.path import dirname, join

from setuptools import setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


if __name__ == "__main__":
    setup(
        use_scm_version={
            'local_scheme': 'dirty-tag',
            'write_to': 'src/setuptools_build_subpackage/_version.py',
            'fallback_version': '1.0.0',
        },
        long_description='%s\n%s'
        % (
            read('README.rst'),
            re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')),
        ),
    )
