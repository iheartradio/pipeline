"""Test message-related functionality."""

from collections import namedtuple
from datetime import datetime

import pytest

from pipeline import nosjify, prepare_message, send_error, send_message

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

Message = namedtuple('Message', ('body',))


def test_prepare_message_adds_job_id():
    """Test that prepare_message adds a job id."""
    actual = prepare_message({}, app_name='testing', event='tested')
    assert 'job_id' in actual


def test_prepare_message_adds_originated_at():
    """Test that prepare_message adds an initial timestamp."""
    actual = prepare_message({}, app_name='testing', event='tested')
    assert 'originated_at' in actual


def test_prepare_message_adds_updated_at():
    """Test that prepare_message adds an updated timestamp."""
    actual = prepare_message({}, app_name='testing', event='tested')
    assert 'updated_at' in actual


def test_prepare_message_originated_at_is_datetime():
    """Test that the initial timestamp is a datetime."""
    actual = prepare_message({}, app_name='testing', event='tested')
    assert isinstance(
        datetime.strptime(actual['originated_at'], DATETIME_FORMAT), datetime)


def test_prepare_message_preserves_job_id():
    """Test that prepare_message preserves the existing job id."""
    actual = prepare_message({'job_id': 1}, app_name='testing', event='tested')
    assert actual['job_id'] == 1


def test_prepare_message_preserves_originated_at():
    """Test that prepare_message preserves the initial timestamp."""
    actual = prepare_message(
        {'originated_at': 'now'}, app_name='testing', event='tested')
    assert actual['originated_at'] == 'now'


def test_prepare_message_replaces_empty_job_id():
    """Test that prepare_message replaces an empty job id."""
    actual = prepare_message(
        {'job_id': None}, app_name='testing', event='tested')
    assert actual['job_id'] is not None


def test_prepare_message_sets_app_name():
    """Test that _prepare messages sets a new app name."""
    actual = prepare_message(
        {'app': 'old_app'}, app_name='testing', event='tested')
    assert actual['app'] == 'testing'


def test_prepare_message_sets_event():
    """Test that _prepare messages sets a new event."""
    actual = prepare_message(
        {'event': 'old_event'}, app_name='testing', event='tested')
    assert actual['event'] == 'tested'


def test_prepare_messages_sets_updated_at():
    """Test that prepare_message sets a new updated timestamp."""
    actual = prepare_message(
        {'updated_at': 'now'}, app_name='testing', event='tested')
    assert actual['updated_at'] != 'now'


def test_prepare_message_updated_at_is_datetime():
    """Test that the updated timestamp is a datetime."""
    actual = prepare_message({}, app_name='testing', event='tested')
    assert isinstance(
        datetime.strptime(actual['updated_at'], DATETIME_FORMAT), datetime)


@pytest.mark.asyncio
async def test_send_error(test_producer):
    """Test that the provided message is sent."""
    expected = {'message': 'test_message'}
    await send_error(expected, producer=test_producer)
    actual = await nosjify(None, Message(test_producer.sent_error))

    assert actual['message'] == expected['message']


@pytest.mark.asyncio
async def test_send_message(test_producer):
    """Test that the provided message is sent."""
    expected = {'message': 'test_message'}
    await send_message(expected, producer=test_producer, event='tested')
    actual = await nosjify(None, Message(test_producer.sent_message))

    assert actual['message'] == expected['message']
