from distutils.command.build import build as orig


class build(orig):
    # Ensure that each dist is built in it's own sub-folder -- if they used the
    # default `build/` then earlier builds would get included in later ones.
    def finalize_options(self):
        # Only change if it's the default
        if self.build_base == 'build':
            self.build_base = f'build/{self.distribution.metadata.name}'
        super().finalize_options()
