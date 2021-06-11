from distutils.core import setup
import distutils.cmd
import setuptools.command.build_py
import subprocess


class LocalizationCommand(distutils.cmd.Command):
    """Create localization files."""

    description = 'Create localization files'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        subprocess.run(['sh', './scripts/localization.sh'])


class CheckCommand(distutils.cmd.Command):
    """Check flake8, pydocstyle and run tests."""

    description = 'Check flake8, pydocstyle and run tests'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        subprocess.run(['sh', './scripts/check.sh'])


class BuildPyCommand(setuptools.command.build_py.build_py):
  """Custom build command."""

  def run(self):
    self.run_command('localization')
    setuptools.command.build_py.build_py.run(self)


setup(
    name='dl_markup',
    version='0.0.1',
    packages=['dl_markup', ],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'dl_markup = dl_markup.__main__:main',
        ],
    },
    cmdclass={
        'localization': LocalizationCommand,
        'check': CheckCommand,
        'build_py': BuildPyCommand,
    },
    package_data={
        "dl_markup": ["*/*.qm"],
    },
)
