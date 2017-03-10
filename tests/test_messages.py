"""Test message-related functionality."""

from collections import namedtuple
from datetime import datetime
import uuid

import pytest

from pipeline import (
    fanout,
    nosjify,
    prepare_incoming_message,
    prepare_outgoing_message,
    send_error,
    send_message,
)

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

Message = namedtuple('Message', ('body',))


@pytest.mark.asyncio
async def test_events_is_added(test_app):
    """Test that the events list is added to messages without it."""
    actual = await prepare_incoming_message(test_app, {})
    assert 'events' in actual


def test_fanout_adds_ancestor_id():
    """Test that fanout adds the original job_id as an ancestor_id."""
    original = {'job_id': 1, 'ancestor_ids': []}
    result = fanout(original)
    assert original['job_id'] in result['ancestor_ids']


def test_fanout_does_not_change_original_message():
    """Test that fanout doesn't change the original message."""
    expected = 1
    original = {'job_id': expected, 'ancestor_ids': []}
    result = fanout(original)
    assert original['job_id'] == expected


def test_fanout_new_job_id():
    """Test that fanout assigns a new job_id."""
    original = {'job_id': 1, 'ancestor_ids': []}
    result = fanout(original)
    assert result['job_id'] != original['job_id']


@pytest.mark.asyncio
async def test_job_id_is_added(test_app):
    """Test that a job id is added to messages without one."""
    actual = await prepare_incoming_message(test_app, {})
    assert 'job_id' in actual


@pytest.mark.asyncio
async def test_job_id_is_preserved(test_app):
    """Test that existing job ids are preserved."""
    actual = await prepare_incoming_message(test_app, {'job_id': 1})
    assert actual['job_id'] == 1


@pytest.mark.asyncio
async def test_message_is_hoisted_to_previous_event(test_app):
    """Test that the message is copied to the previous event."""
    actual = await prepare_incoming_message(
        test_app, {'events': [{}], 'message': 1})
    assert actual['events'][-2]['message'] == 1


@pytest.mark.parametrize('key', (
    'app',
    'event_id',
    'received_at',
))
@pytest.mark.asyncio
async def test_new_event_has_field(key, test_app):
    """Test that the new event has the specified field."""
    actual = await prepare_incoming_message(test_app, {})
    assert actual['events'][-1][key]


@pytest.mark.asyncio
async def test_new_event_is_added(test_app):
    """Test that a new event is added."""
    actual = await prepare_incoming_message(
        test_app, {'events': [{}], 'message': ''})
    assert len(actual['events']) == 2


@pytest.mark.asyncio
async def test_new_event_received_at_is_datetime(test_app):
    """Test that the new event's received timestamp is a datetime."""
    actual = await prepare_incoming_message(test_app, {})
    assert isinstance(datetime.strptime(
        actual['events'][-1]['received_at'], DATETIME_FORMAT), datetime)


def test_new_event_updated_at_is_datetime(test_app):
    """Test that the new event's updated timestamp is a datetime."""
    actual = prepare_outgoing_message({'events': [{}]})
    assert isinstance(datetime.strptime(
        actual['events'][-1]['updated_at'], DATETIME_FORMAT), datetime)


@pytest.mark.asyncio
async def test_originated_at_is_datetime(test_app):
    """Test that the initial timestamp is a datetime."""
    actual = await prepare_incoming_message(test_app, {})
    assert isinstance(
        datetime.strptime(actual['originated_at'], DATETIME_FORMAT), datetime)


@pytest.mark.asyncio
async def test_originated_at_is_preserved(test_app):
    """Test that existing initial timestamps are preserved."""
    actual = await prepare_incoming_message(test_app, {'originated_at': 1})
    assert actual['originated_at'] == 1


@pytest.mark.asyncio
async def test_send_error(test_producer):
    """Test that the provided message is sent."""
    expected = {'message': 'test_message', 'events': [{}]}
    await send_error(expected, producer=test_producer)
    actual = await nosjify(None, Message(test_producer.sent_error))

    assert actual['message'] == expected['message']


@pytest.mark.asyncio
async def test_send_message(test_producer):
    """Test that the provided message is sent."""
    expected = {'message': 'test_message', 'events': [{}]}
    await send_message(expected, producer=test_producer)
    actual = await nosjify(None, Message(test_producer.sent_message))

    assert actual['message'] == expected['message']
