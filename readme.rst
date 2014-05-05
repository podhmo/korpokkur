mako_scaffold
========================================

mako-scaffold

mako-scaffold has several subcommands. list below.

- list
- create
- scan



list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    $ mako-scaffold list
    simple-package -- tiny python package scaffold (this is sample)

create
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    $ mako-scaffold create simple-package .
    package? :foo
    ## foo package is generated

sometime, it's annoying that asking via interactive shell when unknown setting is found.
so, enable to passing value by config file.

.. code:: python

    $ mako-scaffold create --config ./foo.ini simple-package .

.. code:: foo.ini

    [scaffold]
    package = foo

or json file is also ok.

.. code:: python

    $ mako-scaffold create --config ./foo.json simple-package .

.. code:: foo.ini

    {"package": "foo"}


scan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

scan is dry-run operation about create.

.. code:: python

    $ mako-scaffold scan simple-package .
    package? :foo
    d[c]:/tmp/foo
    f[m]: /~/mako_scaffold/scaffolds/simple_package/+package+/setup.py.tmpl -> /tmp/foo/setup.py
    ----------------------------------------
    {
      "package": "foo"
    }

output information what files are generated and what values are asked.
