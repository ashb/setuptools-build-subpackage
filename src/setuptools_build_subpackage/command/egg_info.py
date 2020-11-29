import os
from typing import Optional

from setuptools.command import egg_info as orig
from setuptools.command.sdist import walk_revctrl

from setuptools_build_subpackage.command.sdist import sdist


class egg_info(orig.egg_info):
    def find_sources(self):
        """Generate SOURCES.txt manifest file"""
        # There is no way of sub-classing this, it calls it _directly_
        # Delete the file, so any _bad_ values from previous run don't keep getting copied across
        manifest_filename = os.path.join(self.egg_info, "SOURCES.txt")
        if os.path.exists(manifest_filename):
            self.delete_file(manifest_filename)

        mm = manifest_maker(self.distribution)
        mm.ensure_finalized()
        mm.manifest = manifest_filename

        mm.run()
        self.filelist = mm.filelist


class manifest_maker(orig.manifest_maker):
    manifest: Optional[str] = None
    template: Optional[str] = None

    def finalize_options(self):
        if self.manifest is None:
            self.manifest = os.path.join(self.distribution.subpackage_folder, "MANIFEST")
        if self.template is None:
            self.template = os.path.join(self.distribution.subpackage_folder, "MANIFEST.in")
        return super().finalize_options()

    def prune_file_list(self):
        # Don't include setup.py/.cfg/pyproject.toml from the top-level!
        self.filelist.exclude_pattern(r"^setup\.(py|cfg)$", is_regex=True)
        self.filelist.exclude_pattern(r"^pyproject\.toml$", is_regex=True)
        self.filelist.exclude_pattern(r"^README\..*", is_regex=True)

        # Don't include the setup.cfg from the sub-folder, we'll handle that speically later
        # This could come if there setuptools_scm is installed
        self.filelist.exclude_pattern(os.path.join(self.distribution.subpackage_folder, "setup.cfg"), is_regex=False)

        return super().prune_file_list()

    def write_manifest(self):
        """Extend the manifest file (``SOURCES.txt``) so that it includes files
        that would be written at the top level"""
        old_files = self.filelist.files[:]

        try:
            if self.filelist.files:
                # Only extend it if we've actually populated it, otherwise allow writing an empty manifest
                self.filelist.extend(['setup.py', 'setup.cfg'])

            # TODO: Add in reference to the README from the subfolder, if there is one.
            self.filelist.sort()
            super().write_manifest()
        finally:
            self.filelist.files = old_files

    def add_defaults(self):
        """
        Like setuptools' add_defaults, but only walk revision control files from subfolder, not whole dist
        """
        sdist.add_defaults(self)
        self.check_license()
        self.filelist.append(self.template)
        self.filelist.append(self.manifest)
        rcfiles = list(walk_revctrl(self.distribution.subpackage_folder))
        if rcfiles:
            self.filelist.extend(rcfiles)
        elif os.path.exists(self.manifest):
            self.read_manifest()

        ei_cmd = self.get_finalized_command('egg_info')
        self.filelist.graft(ei_cmd.egg_info)
