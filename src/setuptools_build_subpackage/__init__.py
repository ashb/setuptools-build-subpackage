import os

from setuptools import Distribution as orig

try:
    from ._version import version as __version__  # noqa: F401
except ImportError:
    # In development
    pass

__all__ = [
    'Distribution',
]


class Distribution(orig):

    OPT_NAME = "subpackage-folder"

    global_options = orig.global_options + [
        (f"{OPT_NAME}=", None, "Operate on a subpackage, not the main dist"),
    ]

    def finalize_options(self):
        from .command.build import build
        from .command.egg_info import egg_info
        from .command.sdist import sdist

        super().finalize_options()
        self.cmdclass.setdefault('sdist', sdist)
        self.cmdclass.setdefault('egg_info', egg_info)
        self.cmdclass.setdefault('build', build)

    def find_config_files(self):
        # Make sure we don't load the top-level setup.cfg, but instead the one
        # from the provided folder.
        files = super().find_config_files()

        local_file = None

        # This is called before CLI args are parsed, so we have to have a simplistic arg parser here.
        for i, arg in enumerate(self.script_args):
            if arg == f"--{self.OPT_NAME}":
                local_file = self.script_args[i + 1]
                del self.script_args[i : i + 2]
                break
            elif arg.startswith(f"--{self.OPT_NAME}="):
                local_file = arg[len(self.OPT_NAME) + 3 :]
                del self.script_args[i]
                break

        if local_file:
            self.subpackage_folder = local_file
            return [f for f in files if f != "setup.cfg"] + [os.path.join(local_file, "setup.cfg")]

        return files
