from setuptools import setup, find_packages
requires = [
    "mako", 
    "configless", 
    ]

testing_extras = [
    "jinja2", 
]

setup(name='korpokkur',
      version='0.1',
      url="https://github.com/podhmo/korpokkur", 
      description='scaffolding',
      long_description="", 
      author='podhmo',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(exclude=["tests"]),
      install_requires = requires,
      extras_require = {
          'testing':testing_extras,
          },
      include_package_data=True, 
      test_suite='korpokkur.tests',
      entry_points = """
      [console_scripts]
      korpokkur = korpokkur.command:main
      [korpokkur.scaffold]
      package = korpokkur.scaffolds.package:Package
      nestedpackage = korpokkur.scaffolds.nestedpackage:Package
      scaffold = korpokkur.scaffolds.scaffold:Template
      nestedscaffold = korpokkur.scaffolds.nestedscaffold:Template
      [korpokkur.partial.scaffold]
      """,
      )
