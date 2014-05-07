from setuptools import setup, find_packages
requires = [
    "mako", 
    "zope.interface"
    ]

setup(name='korpokkur',
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
      test_suite="korpokkur.tests", 
      entry_points = """
      [console_scripts]
      korpokkur = korpokkur.command:main
      [korpokkur.scaffold]
      package = korpokkur.scaffolds.package:Package
      scaffold = korpokkur.scaffolds.scaffold:Template
      """,
      )
