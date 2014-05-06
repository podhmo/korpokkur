korpokkur
========================================

korpokkur

korpokkur has several subcommands. list below.

- list
- create
- scan



list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    $ korpokkur list
    simple-package -- tiny python package scaffold (this is sample)

create
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    $ korpokkur create simple-package .
    package? :foo
    ## foo package is generated

sometime, it's annoying that asking via interactive shell when unknown setting is found.
so, enable to pass value by config file.

.. code:: python

    $ korpokkur create --config ./foo.ini simple-package .

.. code:: foo.ini

    [scaffold]
    package = foo

or json file is also ok.

.. code:: python

    $ korpokkur create --config ./foo.json simple-package .

.. code:: foo.ini

    {"package": "foo"}


scan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

scan is dry-run operation about create.

.. code:: python

    $ korpokkur scan simple-package .
    package? :foo
    d[c]:/tmp/foo
    f[m]: /~/korpokkur/scaffolds/simple_package/+package+/setup.py.tmpl -> /tmp/foo/setup.py
    ----------------------------------------
    {
      "package": "foo"
    }

output information what files are generated and what values are asked.
