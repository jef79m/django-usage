=============================
django-usage
=============================

.. image:: https://badge.fury.io/py/django-usage.png
    :target: https://badge.fury.io/py/django-usage

.. image:: https://travis-ci.org/nswrdn/django-usage.png?branch=master
    :target: https://travis-ci.org/nswrdn/django-usage

Track user activity in your project as time spent.

Documentation
-------------

The full documentation is at https://django-usage.readthedocs.org.

Quickstart
----------

Install django-usage::

    pip install django-usage

Add to your installed-apps::

    INSTALLED_APPS += ['usage', ]


Run migrations::

    manage.py migrate usage

Periodically summarize page hits::

    manage.py summarizeusage

If you want to use the demo summary, add a URL::

    url(r'^admin/usage/', usage_display, name='usage.usage_display')

Optional settings::

    USAGE_INTERVAL = 5  # summary interval in minutes
    USAGE_EXCLUDE_URLS = [] # Skip URLS containing these strings when summarizing
    USAGE_DELETE_AFTER = 14 # Delete hit records after this many days.


Features
--------

* TODO

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
