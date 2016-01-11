"""Test jsonify."""

from collections import namedtuple

import pytest

from pipeline import jsonify, nosjify

Message = namedtuple('Message', ('body',))


@pytest.mark.asyncio
@pytest.mark.parametrize('expected', (
    {'a': 1, 'b': 'c'},
    {'a': {'b': {'c': 'd'}}},
    [1, 2, 3, 4],
    'a',
    1,
))
async def test_jsonify(test_app, expected):
    """Test jsonify."""
    intermediate = await jsonify(test_app, expected)
    message = Message(intermediate)
    actual = await nosjify(test_app, message)
    assert actual == expected
    assert actual != intermediate
