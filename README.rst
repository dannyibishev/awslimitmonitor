===============
awslimitmonitor
===============

A Python script which makes api calls to AWS (using boto3). The script gathers information about the services used, the limits set for that resource, and also returns a status which lets you know how close you are to the set limit.

Installation
------------

.. code-block:: sh

    $ pip install awslimitmonitor

Usage
-----

If you ever need to see what options are available. Type:

To check all limits you can do:

.. code-block:: sh

    $ awslimitmonitor all

You can also check limits individually. example:

.. code-block:: sh

    $ awslimitmonitor ec2
    ... <output from the script>
    $ awslimitmonitor rds
    ... <output from the script>

To see what options are available, alongside usage instructions. Type:

.. code-block:: sh

    $ awslimitmonitor -h

To check the version of the script:

.. code-block:: sh

    $ awslimitmonitor -v
    $ awslimitmonitor --version
