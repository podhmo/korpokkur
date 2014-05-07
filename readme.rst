korpokkur
========================================

korpokkur is command tool set for scaffold.


(only support 2.7 and 3.3

korpokkur has several subcommands. list below.

- list
- create
- scan


list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ korpokkur list
    package -- tiny python package scaffold (this is sample)
    scaffold -- korpokkur scaffold template template

create
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ korpokkur create package .
    package (package name)[sample]:foo
    version (version number for project)[0.0]:0.1
    description (package description)[-]:sample package

    $ tree foo
    foo
    |-- CHANGES.txt
    |-- README.rst
    |-- foo
    |   `-- tests
    |       `-- __init__.py
    `-- setup.py

sometime, it's annoying that asking via interactive shell when unknown setting is found.
so, enable to pass value by config file.

.. code:: bash

    $ korpokkur create --config ./foo.ini package .

.. code:: foo.ini

    [scaffold]
    package = foo
    version = 0.1
    description = sample package

or json file is also ok.

.. code:: bash

    $ korpokkur create --config ./foo.json package .

.. code:: foo.ini

    {"package": "foo", "version": "0.1", "sample package"}


scan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

scan is dry-run operation about create.

.. code:: bash

    $ korpokkur scan package
    package (package name)[sample]:foo
    d[c]: /tmp/foo
    d[c]: /tmp/foo/foo
    f[c]: ~/korpokkur/scaffolds/package/+package+/CHANGES.txt -> /tmp/foo/CHANGES.txt
    f[m]: ~/korpokkur/scaffolds/package/+package+/README.rst.tmpl -> /tmp/foo/README.rst
    f[m]: ~/korpokkur/scaffolds/package/+package+/setup.py.tmpl -> /tmp/foo/setup.py
    version (version number for project)[0.0]:0.1
    description (package description)[-]:sample package
    d[c]: /tmp/foo/foo/tests
    f[c]: ~/korpokkur/scaffolds/package/+package+/+package+/tests/__init__.py -> /tmp/foo/foo/tests/__init__.py
    f[c]: ~/korpokkur/scaffolds/pygitignore/+package+/.gitignore -> /tmp/foo/.gitignore
    ----------------------------------------
    *input values*
    {
      "version": "0.1", 
      "package": "foo", 
      "description": "sample package"
    }

output information what files are generated and what values are asked.
