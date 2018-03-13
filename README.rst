================
Django CMS LayoutTools
================


|pypi| |build| |coverage|

**Django CMS LayoutTools** is a set of plugins for `django CMS <http://django-cms.org>`_
that allows you to design content sections on cms webpages that have specified 
container properties (e.g., container-fluid) and css styling such as backgrounds.
It uses Bootstrap3 container classes by default, but doesn't necessarily require
Bootstrap to be a useful tool for sectioning and styling content. A Section plugin
is provided now, but further plugins may be created at a later date.

It uses images/files managed by `Django Filer <https://github.com/divio/django-filer>`_.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. See the github repo 
`contribution guidelines https://github.com/mci/djangocms-layouttools>`_.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/mci/djangocms-layouttools/blob/master/setup.py>`_
file for additional dependencies:

* Python 2.7, 3.3 or higher
* Django 1.8 or higher
* Django Filer 1.2.4 or higher

Make sure `django Filer <http://django-filer.readthedocs.io/en/latest/installation.html>`_
is installed and configured appropriately.


Installation
------------

For a manual install:

* run ``pip install djangocms-layouttools``
* add ``djangocms_layouttools`` to your ``INSTALLED_APPS``
* run ``python manage.py migrate djangocms_layouttools``


Configuration
-------------

TBD


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |pypi| image:: https://badge.fury.io/py/djangocms-layouttools.svg
    :target: http://badge.fury.io/py/djangocms-layouttools
.. |build| image:: https://travis-ci.org/mci/djangocms-layouttools.svg?branch=master
    :target: https://travis-ci.org/mci/djangocms-layouttools
