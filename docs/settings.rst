========
Settings
========

pipeline provides settings that are commonly used across many
services. To use these settings::

    from decouple import config
    from pipeline.settings import *  # NOQA

    # Continue to define other settings below
    SERVICE_SPECIFIC_SETTING = config('SERVICE_SETTING', default='foo')

Available Settings
==================

The following settings are provided. All settings are mandatory unless a
default is specified.

+----------------------------+------------------------------------------------+
| ``KAFKA_ASYNC``            | Whether or not the Kafka producer should batch |
|                            | send messages                                  |
|                            | default: ``False``                             |
+----------------------------+------------------------------------------------+
| ``KAFKA_BATCH_SEND_COUNT`` | The producer batch size (if batch sending is   |
|                            | enabled)                                       |
|                            | default: ``20``                                |
+----------------------------+------------------------------------------------+
| ``KAFKA_BATCH_SEND_TIME``  | The maximum amount of time (in seconds) to     |
|                            | wait before producing a batch of messages      |
|                            | default: ``60``                                |
+----------------------------+------------------------------------------------+
| ``KAFKA_BROKER_HOST``      | The hostname of the Kakfa broker               |
+----------------------------+------------------------------------------------+
| ``KAFKA_BROKER_PORT``      | The port the Kafka broker is listening on      |
|                            | default: ``9092``                              |
+----------------------------+------------------------------------------------+
| ``KAFKA_GROUP_NAME``       | The group the consumer is part of              |
+----------------------------+------------------------------------------------+
| ``KAFKA_TOPIC_INBOUND``    | The topic to consume from                      |
|                            | default: ``""``                                |
+----------------------------+------------------------------------------------+
| ``KAFKA_TOPIC_OUTBOUND``   | The topic to produce to                        |
+----------------------------+------------------------------------------------+
| ``LOG_HANDLER``            | The class of the log handler as a string       |
|                            | default: ``'logstash.TCPLogstashHandler'``     |
+----------------------------+------------------------------------------------+
| ``LOG_HANDLER_KWARGS``     | Dict of kwargs to pass to the log handler      |
|                            | default:``{                                    |
|                            | 'host': decouple.config('LOGSTASH_HOST'),      |
|                            | 'port': decouple.config('LOGSTASH_PORT'),      |
|                            | 'version': decouple.config('LOGSTASH_VERSION') |
|                            | }``                                            |
+----------------------------+------------------------------------------------+
