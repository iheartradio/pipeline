"""Common utilities for the Ingestion Pipeline."""

from datetime import datetime
import uuid

__all__ = ('ignore_provider', 'prepare_message', 'send_message')


def ignore_provider(provider, included=None, excluded=None):
    """Return whether a provider should be ignored.

    If ``included`` is not empty, this function will return ``False``
    for any provider in the list and ``True`` for all other providers.
    The provider will only be checked against ``excluded`` when
    ``included`` is empty.

    Args:
        provider (str): The identifier of the provider to check.
        included (list, optional): A list of all providers not to
          ignore.
        excluded (list, optional): A list of providers that should be
          ignored.

    Returns:
        bool: True if the provider should be ignored.
    """
    if included:
        # If there is a list of included providers, it is the only thing
        # checked to determine whether or not to ignore the provider.
        return provider not in included

    return provider in (excluded or ())


def prepare_message(message, *, app_name, event):
    """Return a message with the common message structure.

    Args:
        message (dict): The message to prepare.
        app_name (str): The name of the application sending the message.
        event (str): The name of the event that created the message.

    Returns:
        dict: The prepared message.

    .. versionadded:: 0.2.0
    """
    # Make sure the job id exists and has a value.
    if not message.get('job_id'):
        message['job_id'] = str(uuid.uuid4())
    message['app'] = app_name
    message['event'] = event
    message['updated_at'] = datetime.utcnow().isoformat()
    # Make sure the origination time exists and has a value.
    if not message.get('originated_at'):
        message['originated_at'] = message['updated_at']
    return message


def send_message(message, *, producer, event):
    """Send an outgoing message.

    ``message`` will be updated with the common message structure and
    sent through the specified producer.

    Args:
        message (dict): The message to send.
        producer: The product through which to send the message.
        event (str): The name of the event that created the message.

    .. versionadded:: 0.2.0
    """
    prepared_message = prepare_message(
        message, app_name=producer.app_name, event=event)
    producer.send(prepared_message)
