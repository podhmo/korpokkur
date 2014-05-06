from setuptools import setup, find_packages
requires = [
    "mako", 
    "zope.interface"
    ]

setup(name='mako_scaffold',
      version='0.0.1',
      description='scaffold',
      long_description="", 
      author='podhmo',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
      ],
      package_dir={'': '.'},
      packages=find_packages('.'),
      install_requires = requires,
      test_suite="mako_scaffold.tests", 
      entry_points = """
      [console_scripts]
      mako-scaffold = mako_scaffold.command:main
      [mako.scaffold]
      simple-package = mako_scaffold.scaffolds.simple_package:Package
      py-gitignore
      """,
      )
