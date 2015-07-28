=======
Schemas
=======

pipeline provides validation schemas for many common data structures used by
services. To use a schema to validate a dictionary::

    from pipeline.schema import artist

    doc = {'name': 'pipeline artist'}
    artist(doc)

In order to handle validation errors yourself, you will need to wrap the check
in a try/except block::

    from pipeline.schema import artist, MultipleInvalid

    doc = {'invalid-field': 'invalid'}
    try:
        artist(doc)
    except MultipleInvalid:
        logging.error('The artist was invalid.')

Available schemas
=================

.. automodule:: pipeline.schema
   :members:
