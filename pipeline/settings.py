"""Settings common to all pipeline services."""

from decouple import config

KAFKA_ASYNC = config('KAFKA_ASYNC', cast=bool, default=False)
KAFKA_BATCH_SEND = config('KAFKA_BATCH_SEND', cast=bool, default=False)
KAFKA_BATCH_SEND_COUNT = config('KAFKA_BATCH_SEND_COUNT', cast=int, default=20)
KAFKA_BATCH_SEND_TIME = config('KAFKA_BATCH_SEND_TIME', cast=int, default=60)
KAFKA_BROKER_HOST = config('KAFKA_BROKER_HOST')
KAFKA_BROKER_PORT = config('KAFKA_BROKER_PORT', cast=int, default=9092)
KAFKA_GROUP_NAME = config('KAFKA_GROUP_NAME')
KAFKA_TOPIC_INBOUND = config('KAFKA_TOPIC_INBOUND', default='""')
KAFKA_TOPIC_OUTBOUND = config('KAFKA_TOPIC_OUTBOUND')
LOG_HANDLER = 'logstash.TCPLogstashHandler'
LOG_HANDLER_KWARGS = {
    'host': config('LOGSTASH_HOST'),
    'port': config('LOGSTASH_PORT', cast=int),
    'version': config('LOGSTASH_VERSION', cast=int, default=1),
}

# Remove config after use to keep it out of the namespace
del config
