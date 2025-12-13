import os

from setuptools import setup
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()

    def get_tag(self):
        if "BUILD" in os.environ and os.environ["BUILD"] == "universal":
            return super().get_tag()
        self.root_is_pure = False
        python, abi, platform = super().get_tag()
        self.root_is_pure = True
        pure_python, pure_abi, pure_platform = super().get_tag()
        return pure_python, pure_abi, platform.replace("linux", "manylinux1")


setup(cmdclass={"bdist_wheel": bdist_wheel})
