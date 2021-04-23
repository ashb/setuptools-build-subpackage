import os
import tarfile
import textwrap
from pathlib import Path

import setuptools
from wheel.wheelfile import WheelFile

from setuptools_build_subpackage import Distribution

ROOT = Path(__file__).parent.parent


def build_dist(folder, command, output, *args):
    args = [
        '--subpackage-folder',
        folder,
        'clean',
        '--all',
        command,
        '--dist-dir',
        output,
        *args,
    ]
    cur = os.getcwd()
    os.chdir('example')

    try:
        setuptools.setup(
            distclass=Distribution,
            script_args=args,
        )
    finally:
        os.chdir(cur)


def test_bdist_wheel(tmp_path):

    build_dist('example/sub_module_a', 'bdist_wheel', tmp_path)
    build_dist('example/sub_module_b', 'bdist_wheel', tmp_path)

    wheel_a_path = tmp_path / 'example_sub_moudle_a-0.0.0-py2.py3-none-any.whl'
    wheel_b_path = tmp_path / 'example_sub_moudle_b-0.0.0-py2.py3-none-any.whl'

    assert wheel_a_path.exists(), "sub_module_a wheel file exists"
    assert wheel_b_path.exists(), "sub_module_b wheel file exists"

    with WheelFile(wheel_a_path) as wheel_a:
        assert set(wheel_a.namelist()) == {
            'example/sub_module_a/__init__.py',
            'example/sub_module_a/where.py',
            'example_sub_moudle_a-0.0.0.dist-info/AUTHORS.rst',
            'example_sub_moudle_a-0.0.0.dist-info/LICENSE',
            'example_sub_moudle_a-0.0.0.dist-info/METADATA',
            'example_sub_moudle_a-0.0.0.dist-info/WHEEL',
            'example_sub_moudle_a-0.0.0.dist-info/top_level.txt',
            'example_sub_moudle_a-0.0.0.dist-info/RECORD',
        }

        where = wheel_a.open('example/sub_module_a/where.py').read()
        assert where == b'a = "module_a"\n'

    with WheelFile(wheel_b_path) as wheel_b:
        assert set(wheel_b.namelist()) == {
            'example/sub_module_b/__init__.py',
            'example/sub_module_b/where.py',
            'example_sub_moudle_b-0.0.0.dist-info/AUTHORS.rst',
            'example_sub_moudle_b-0.0.0.dist-info/LICENSE',
            'example_sub_moudle_b-0.0.0.dist-info/METADATA',
            'example_sub_moudle_b-0.0.0.dist-info/WHEEL',
            'example_sub_moudle_b-0.0.0.dist-info/top_level.txt',
            'example_sub_moudle_b-0.0.0.dist-info/RECORD',
        }

        where = wheel_b.open('example/sub_module_b/where.py').read()
        assert where == b'a = "module_b"\n'


def test_sdist(tmp_path):
    # Build both dists in the same test, so we can check there is no cross-polution
    build_dist('example/sub_module_a', 'sdist', tmp_path)
    build_dist('example/sub_module_b', 'sdist', tmp_path)

    sdist_a_path = tmp_path / 'example_sub_moudle_a-0.0.0.tar.gz'
    sdist_b_path = tmp_path / 'example_sub_moudle_b-0.0.0.tar.gz'

    assert sdist_a_path.exists(), "sub_module_a sdist file exists"
    assert sdist_b_path.exists(), "sub_module_b sdist file exists"

    with tarfile.open(sdist_a_path) as sdist_a:
        assert set(sdist_a.getnames()) == {
            'example_sub_moudle_a-0.0.0',
            'example_sub_moudle_a-0.0.0/AUTHORS.rst',
            'example_sub_moudle_a-0.0.0/LICENSE',
            'example_sub_moudle_a-0.0.0/PKG-INFO',
            'example_sub_moudle_a-0.0.0/example',
            'example_sub_moudle_a-0.0.0/example/sub_module_a',
            'example_sub_moudle_a-0.0.0/example/sub_module_a/__init__.py',
            'example_sub_moudle_a-0.0.0/example/sub_module_a/where.py',
            'example_sub_moudle_a-0.0.0/example_sub_moudle_a.egg-info',
            'example_sub_moudle_a-0.0.0/example_sub_moudle_a.egg-info/PKG-INFO',
            'example_sub_moudle_a-0.0.0/example_sub_moudle_a.egg-info/SOURCES.txt',
            'example_sub_moudle_a-0.0.0/example_sub_moudle_a.egg-info/dependency_links.txt',
            'example_sub_moudle_a-0.0.0/example_sub_moudle_a.egg-info/not-zip-safe',
            'example_sub_moudle_a-0.0.0/example_sub_moudle_a.egg-info/top_level.txt',
            'example_sub_moudle_a-0.0.0/setup.cfg',
            'example_sub_moudle_a-0.0.0/setup.py',
        }

        where = sdist_a.extractfile('example_sub_moudle_a-0.0.0/example/sub_module_a/where.py').read()
        assert where == b'a = "module_a"\n'

        setup_cfg = sdist_a.extractfile('example_sub_moudle_a-0.0.0/setup.cfg').read().decode('ascii')

        assert setup_cfg == (ROOT / 'example' / 'example' / 'sub_module_a' / 'setup.cfg').open(encoding='ascii').read()

    with tarfile.open(sdist_b_path) as sdist_b:
        assert set(sdist_b.getnames()) == {
            'example_sub_moudle_b-0.0.0',
            'example_sub_moudle_b-0.0.0/AUTHORS.rst',
            'example_sub_moudle_b-0.0.0/LICENSE',
            'example_sub_moudle_b-0.0.0/PKG-INFO',
            'example_sub_moudle_b-0.0.0/example',
            'example_sub_moudle_b-0.0.0/example/sub_module_b',
            'example_sub_moudle_b-0.0.0/example/sub_module_b/__init__.py',
            'example_sub_moudle_b-0.0.0/example/sub_module_b/where.py',
            'example_sub_moudle_b-0.0.0/example_sub_moudle_b.egg-info',
            'example_sub_moudle_b-0.0.0/example_sub_moudle_b.egg-info/PKG-INFO',
            'example_sub_moudle_b-0.0.0/example_sub_moudle_b.egg-info/SOURCES.txt',
            'example_sub_moudle_b-0.0.0/example_sub_moudle_b.egg-info/dependency_links.txt',
            'example_sub_moudle_b-0.0.0/example_sub_moudle_b.egg-info/not-zip-safe',
            'example_sub_moudle_b-0.0.0/example_sub_moudle_b.egg-info/top_level.txt',
            'example_sub_moudle_b-0.0.0/setup.cfg',
            'example_sub_moudle_b-0.0.0/setup.py',
        }

        where = sdist_b.extractfile('example_sub_moudle_b-0.0.0/example/sub_module_b/where.py').read()
        assert where == b'a = "module_b"\n'

        setup_cfg = sdist_b.extractfile('example_sub_moudle_b-0.0.0/setup.cfg').read().decode('ascii')

        assert setup_cfg == (ROOT / 'example' / 'example' / 'sub_module_b' / 'setup.cfg').open(encoding='ascii').read()


def test_license_template(tmp_path):
    build_dist('example/sub_module_a', 'sdist', tmp_path, '--license-template', ROOT / 'LICENSE')

    sdist_a_path = tmp_path / 'example_sub_moudle_a-0.0.0.tar.gz'

    assert sdist_a_path.exists(), "sub_module_a sdist file exists"

    with tarfile.open(sdist_a_path) as sdist_a:
        setup_py = sdist_a.extractfile('example_sub_moudle_a-0.0.0/setup.py').read().decode('ascii')

        assert setup_py == textwrap.dedent(
            """\
            # Apache Software License 2.0
            #
            # Copyright (c) 2020, Ash Berlin-Taylor.
            #
            # Licensed under the Apache License, Version 2.0 (the "License");
            # you may not use this file except in compliance with the License.
            # You may obtain a copy of the License at
            #
            # https://www.apache.org/licenses/LICENSE-2.0
            #
            # Unless required by applicable law or agreed to in writing, software
            # distributed under the License is distributed on an "AS IS" BASIS,
            # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
            # See the License for the specific language governing permissions and
            # limitations under the License.

            __import__("setuptools").setup()
            """
        )
