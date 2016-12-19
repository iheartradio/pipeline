"""Common utilities for the Ingestion Pipeline."""

from copy import deepcopy
from datetime import datetime
import json
import uuid

from henson.exceptions import Abort

__all__ = ('ignore_provider', 'jsonify', 'nosjify', 'prepare_incoming_message', 'prepare_outgoing_message', 'send_error', 'send_message')  # noqa


async def ignore_provider(app, message):
    """Return whether a provider should be ignored.

    This function will check for ``INCLUDED_PROVIDERS`` and
    ``EXCLUDED_PROVIDERS`` settings on ``app`` If the former is not
    empty, ``False`` will be returned for any provider in the list and
    ``True`` for all other providers. The provider will only be checked
    against ``EXCLUDED_PROVIDERS`` when the list of included providers
    is empty.

    The schema of the incoming message should be validated before using
    this function.

    Args:
        app (henson.base.Application): The application instance that
            received the message.
        message (dict): The incoming message. It should contain a key
            named ``'provider'``.

    Returns:
        dict: The incoming message.

    Raises:
        henson.exceptions.Abort: The provider should be ignored.
        KeyError: No provider is included in the message.
    """
    provider = message['provider']

    included = app.settings.get('INCLUDED_PROVIDERS')
    if included:
        # If there is a list of included providers, it is the only thing
        # checked to determine whether or not to ignore the provider.
        if provider not in included:
            # If the provider isn't listed, ignore it.
            raise Abort('provider.ignored', message)
    elif provider in (app.settings.get('EXCLUDED_PROVIDERS') or ()):
        # If the provider is listed, ignore it.
        raise Abort('provider.ignored', message)

    return message


async def jsonify(app, message):
    """Return an encoded dictionary.

    Args:
        app (henson.base.Application): The application.
        message (dict): The message to encode.

    Returns:
        bytes: The encoded message.
    """
    return json.dumps(message).encode('utf-8')


async def nosjify(app, message):
    """Return a decoded dictionary.

    Args:
        app (henson.base.Application): The application.
        message: An object with an attribute called ``body`` containing
            the message to decode.

    Returns:
        dict: The decoded message.
    """
    return json.loads(message.body.decode('utf-8'))


async def prepare_incoming_message(app, message):
    """Prepare the incoming message with the common message structure.

    Messages have the following structure::

        {
            'job_id': ...,
            'originated_at': ...,
            'events': [
                {
                    'app': ...,
                    'event_id': ...,
                    'received_at': ...,
                },
            ],
            'message': ...,
        }

    As part of preparing the message, ``job_id``, ``originated_at``, and
    ``events`` will be added if they don't exist. If ``events`` exists
    and contains events, ``message`` will be hoisted to the last event
    for archival purposes. A new event will be added.

    Args:
        app (henson.base.Application): The application instance that
            received the message.
        message (dict): The incoming message.

    Returns:
        dict: The prepared message.

    .. versionadded:: 1.0.0
    """
    now = datetime.utcnow().isoformat()

    if not message.get('job_id'):
        message['job_id'] = str(uuid.uuid4())

    if not message.get('originated_at'):
        message['originated_at'] = now

    if 'events' not in message:
        message['events'] = []
    elif message['events']:
        message['events'][-1]['message'] = deepcopy(message['message'])

    message['events'].append({
        'app': app.name,
        'event_id': str(uuid.uuid4()),
        'received_at': now,
    })

    return message


def prepare_outgoing_message(message):
    """Return a message with the common message structure.

    Args:
        message (dict): The message to prepare.

    Returns:
        dict: The prepared message.

    .. versionchanged:: 1.0.0

        With the changes made to the common message structure, most of
        the functionality has been moved to
        :func:`prepare_incoming_message`. The ``app_name`` and ``event``
        arguments have been removed and the function has been renamed to
        better distinguish itself from :func:`prepare_incoming_message`.
    """
    message['events'][-1]['updated_at'] = datetime.utcnow().isoformat()
    return message


async def send_error(message, *, producer):
    """Send an error message.

    ``message`` will be updated with the common message structure and
    sent through the specified producer.

    Args:
        message (dict): The message to send.
        producer: The producer through which to send the message.
    """
    # Preserve the incoming event.
    prepared_message = prepare_outgoing_message(message)
    # TODO: This should be done in a separate step.
    serialized_message = await jsonify(producer.app, prepared_message)
    await producer.error(serialized_message)


async def send_message(message, *, producer, event, routing_key=None):
    """Send an outgoing message.

    ``message`` will be updated with the common message structure and
    sent through the specified producer.

    Args:
        message (dict): The message to send.
        producer: The product through which to send the message.
        event (str): The name of the event that created the message.
        routing_key (Optional[str]): The routing key to be passed
            through to the producer's ``send`` method. Defaults to
            ``None``.

    .. versionchanged:: 0.4.0

        The ``routing_key`` argument is now supported.
    """
    prepared_message = prepare_outgoing_message(message)
    # TODO: This should be done in a separate step.
    serialized_message = await jsonify(producer.app, prepared_message)
    await producer.send(serialized_message, routing_key=routing_key)
