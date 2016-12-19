=========
Changelog
=========

Version 1.0.0
=============

Release TBD

- Add ``prepare_incoming_message`` to support the new common message structure
- Rename ``prepare_message`` to ``prepare_outgoing_message`` and remove the
  arguments that are no longer needed with the changes to the common message
  structure (*backwards incompatible*)


Version 0.4.0
=============

Released 2016-09-21

- Make ``duration`` a required field for products
- Add ``routing_key`` argument to ``send_message``

Version 0.3.0
=============

Released 2016-03-14

- Make ``ignore_provider``, ``send_message``, and ``send_error`` into
  coroutines
- Add ``validate_schema`` to handle validating document schemas
- Add additional fields to media schema for audio files
- Remove settings module (*Backward Incompatible*)
- Add ``jsonify`` and ``nosjify`` coroutines for serializing and deserializing
  messages
- Serialize outgoing messages in ``send_message`` and ``send_error``
- Add ``takedown`` and ``delivery`` schemas
- Remove ``windows_drm_id``
- Make media optional
- Set track bundle counts
- Make sub label names optional

Version 0.2.0
=============

Released 2015-11-19

- Add ``prepare_message`` to handle formatting messages with the common message
  structure
- Add ``send_message`` to handle sending messages through the specified
  producer
- Add function to iterate over schema validation error messages
- Add ``send_error`` to handle sending error messages through the specified
  producer
- Add settings module to provide settings available to all pipeline services

Version 0.1.2
=============

Released 2015-08-17

- Move release to track bundle

Version 0.1.1
=============

Released 2015-08-13

- Remove unsupported usage rules

Version 0.1.0
=============

Released 2015-07-31

- Initial release
