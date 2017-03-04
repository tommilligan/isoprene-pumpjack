.. isoprene-pumpjack documentation master file, created by
   sphinx-quickstart on Mon Feb 27 17:32:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

isoprene-pumpjack
=============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Installation
------------

Install with pip::

    pip install isoprene-pumpjack

Use
---

To run with Gunicorn prod server::

    gunicorn isoprene_pumpjack.wsgi:app

To run with Flask dev server::

    isoprene-pumpjack

API
---

.. autoflask:: isoprene_pumpjack:app
   :undoc-static:

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
