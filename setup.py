from setuptools import setup, find_packages
requires = [
    "mako", 
    "zope.interface", 
    ]

testing_extras = [
    "jinja2", 
]

setup(name='korpokkur',
      version='0.0.4',
      url="https://github.com/podhmo/korpokkur", 
      description='scaffolding',
      long_description="", 
      author='podhmo',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(),
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
      scaffold = korpokkur.scaffolds.scaffold:Template
      """,
      )
