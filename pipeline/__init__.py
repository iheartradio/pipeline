"""Common utilities for the Ingestion Pipeline."""

from datetime import datetime
import uuid

__all__ = ('ignore_provider', 'prepare_message', 'send_error', 'send_message')


async def ignore_provider(app, provider):
    """Return whether a provider should be ignored.

    This function will check for ``INCLUDED_PROVIDERS`` and
    ``EXCLUDED_PROVIDERS`` settings on ``app`` If the former is not
    empty, ``False`` will be returned for any provider in the list and
    ``True`` for all other providers. The provider will only be checked
    against ``EXCLUDED_PROVIDERS`` when the list of included providers
    is empty.

    Args:
        app (henson.base.Application): The application instance that
            received the message.
        provider (str): The identifier of the provider to check.

    Returns:
        bool: True if the provider should be ignored.

    .. versionchanged:: 0.3.0

        This function is now a coroutine and can be used as a message
        preprocessor. While it does nothing blocking, regular functions
        can't be used. Its arguments have changed to reflect the
        required signature of a preprocessor.
    """
    included = app.settings.get('INCLUDED_PROVIDERS')
    if included:
        # If there is a list of included providers, it is the only thing
        # checked to determine whether or not to ignore the provider.
        return provider not in included

    return provider in (app.settings.get('EXCLUDED_PROVIDERS') or ())


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


async def send_error(message, *, producer):
    """Send an error message.

    ``message`` will be updated with the common message structure and
    sent through the specified producer.

    Args:
        message (dict): The message to send.
        producer: The product through which to send the message.

    .. versionchanged:: 0.3.0

        This function is now a coroutine.

    .. versionadded:: 0.2.0
    """
    # Preserve the incoming event.
    prepared_message = prepare_message(
        message, app_name=producer.app_name, event=message.get('event'))
    await producer.error(prepared_message)


async def send_message(message, *, producer, event):
    """Send an outgoing message.

    ``message`` will be updated with the common message structure and
    sent through the specified producer.

    Args:
        message (dict): The message to send.
        producer: The product through which to send the message.
        event (str): The name of the event that created the message.

    .. versionchanged:: 0.3.0

        This function is now a coroutine.

    .. versionadded:: 0.2.0
    """
    prepared_message = prepare_message(
        message, app_name=producer.app_name, event=event)
    await producer.send(prepared_message)
