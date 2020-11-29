import os
from distutils.command.sdist import sdist as base
from distutils.errors import DistutilsOptionError
from typing import Optional

from setuptools.command.sdist import sdist as orig


class sdist(orig):
    readme: Optional[str] = None
    license_template: Optional[str] = None

    user_options = orig.user_options + [
        (
            "license-template=",
            None,
            "Path to plain-text license template to include as comment in generated setup.py file",
        ),
    ]

    add_license_comment_to_generated_files = False

    def finalize_options(self):
        if self.manifest is None:
            self.manifest = os.path.join(self.distribution.subpackage_folder, "MANIFEST")
        if self.template is None:
            self.template = os.path.join(self.distribution.subpackage_folder, "MANIFEST.in")

        if self.license_template:
            if not os.path.exists(self.license_template):
                raise DistutilsOptionError("license-template file '%s' not found" % self.license_template)
        return super().finalize_options()

    def check_readme(self):
        for f in self.READMES:
            filename = os.path.join(self.distribution.subpackage_folder, f)
            if os.path.exists(filename):
                self.readme = filename
                return
        else:
            self.warn(
                "standard file not found in "
                + self.distribution.subpackage_folder
                + ": should have one of "
                + ", ".join(self.READMES)
            )

    def make_release_tree(self, base_dir, files):
        self.mkpath(base_dir)
        self.copy_file(
            os.path.join(self.distribution.subpackage_folder, "setup.cfg"),
            base_dir,
        )

        if self.readme:
            # Copy the readme from the subfolder, to the top level of the dist
            self.copy_file(self.readme, base_dir)

        self.make_pep517_stub_setup(base_dir)

        # By-pass setuptools's method -- it copies the wrong setup.cfg
        base.make_release_tree(self, base_dir, files)

    def make_pep517_stub_setup(self, base_dir):
        """Create a stub setup.py so the setup.cfg can be loaded for non PEP-517 installers"""
        with open(os.path.join(base_dir, "setup.py"), "w") as fh:

            if self.license_template:
                with open(self.license_template) as license:
                    for line in license:
                        if line == '\n':
                            # Make sure we don't write `# \n`, just `#\n`
                            fh.write("#\n")
                        else:
                            fh.write(f"# {line}")
                fh.write("\n")
            fh.write('__import__("setuptools").setup()\n')

    def prune_file_list(self):
        # Don't include setup.py/setup.cfg from the top-level
        self.filelist.exclude_pattern(r"^setup\.(py|cfg)", is_regex=True)
        super().prune_file_list()

    def _add_defaults_optional(self):
        """
        We don't want any of the default optional files.

        This is setup.cfg, pyproject.toml, and test/test*.py, all from the
        toplevel, which we don't want.
        """
        pass
