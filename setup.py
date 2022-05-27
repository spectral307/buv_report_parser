from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(name="buv_report_parser",
      version="0.0.0",
      packages=["buv_report_parser"],
      install_requires=requirements)
