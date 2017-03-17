Installation
============

Install with pip::

    pip install isoprene-pumpjack

Use
---

To run with Gunicorn prod server::

    gunicorn isoprene_pumpjack.wsgi:app

To run with Flask dev server::

    isoprene-pumpjack
