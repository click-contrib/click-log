==============================================================
Click-log: Simple and beautiful logging for click applications
==============================================================

.. include:: ../README.rst

.. toctree::
   :maxdepth: 2

.. module:: click_log

Getting started
===============

Assuming you have this Click application::

    @click.command()
    def cli():
        click.echo("Dividing by zero.")

        try:
            1 / 0
        except:
            click.echo("ERROR: Failed to divide by zero.")


Ignore the application's core functionality for a moment. The much more
pressing question here is: How do we add an option to not print anything on
success? We could try this::

    @click.command()
    @click.option('--quiet', default=False, is_flag=True)
    def cli(quiet):
        if not quiet:
            click.echo("Dividing by zero.")

        try:
            1 / 0
        except:
            click.echo("ERROR: Failed to divide by zero.")

Wrapping if-statements around each ``echo``-call is cumbersome though. And with
that, we discover logging::

    import logging
    logger = logging.getLogger(__name__)
    # More setup for logging handlers here

    @click.command()
    @click.option('--quiet', default=False, is_flag=True)
    def cli(quiet):
        if quiet:
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)

        ...

Logging is a better solution, but partly because Python's logging module aims
to be so generic, it doesn't come with sensible defaults for CLI applications.
At some point you might also want to expose more logging levels through more
options, at which point the boilerplate code grows even more.

This is where click-log comes in::

    import logging
    logger = logging.getLogger(__name__)

    @click.command()
    @click_log.simple_verbosity_option()
    @click_log.init(__name__)
    def cli():
        logger.info("Dividing by zero.")

        try:
            1 / 0
        except:
            logger.error("Failed to divide by zero.")

The output will look like this::

    Dividing by zero.
    error: Failed to divide by zero.


The ``error:``-prefix will be red, unless the output is piped to another
command.

Under the hood, click-log will get the logger by the given name, and store it
on the click context object. You can then use :py:func:`get_level` and
:py:func:`set_level`. Those functions will look up the logger from the context
object without you having to pass any logger object or name.

The :py:func:`simple_verbosity_option` decorator adds a ``--verbosity`` option
that takes a (case-insensitive) value of ``DEBUG``, ``INFO``, ``WARNING``,
``ERROR``, or ``CRITICAL``, and calls :py:func:`set_level` accordingly.

API
===

.. autofunction:: init

.. autofunction:: simple_verbosity_option

.. autofunction:: basic_config

.. autofunction:: get_level

.. autofunction:: set_level

Classes
-------

.. autoclass:: ClickHandler

.. autoclass:: ColorFormatter



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

