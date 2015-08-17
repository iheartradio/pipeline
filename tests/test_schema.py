"""Test the schemas."""

import json
import os

import pytest
import voluptuous

from pipeline import schema


def load_json(filename):
    """Return a parsed JSON file.

    Args:
        filename (str): The relative path to the JSON file.

    Returns:
        dict: The parsed JSON file.
    """
    filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        'schema',
        filename)
    with open(filepath) as f:
        doc = json.loads(f.read())
    return doc


def test_empty_document():
    """Test that an empty document doesn't validate."""
    doc = load_json('empty.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_invalid_track_action():
    """Test that a bad track action doesn't validate."""
    doc = load_json('invalid-track-action.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_invalid_track_bundle_action():
    """Test that a bad track bundle action doesn't validate."""
    doc = load_json('invalid-track-bundle-action.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_iter_errors_multipleinvalid():
    """Test that iter_errors handles multiple errors."""
    data = {'a': '1'}
    test_schema = voluptuous.Schema({'a': int, 'b': str}, required=True)
    try:
        test_schema(data)
    except schema.MultipleInvalid as e:
        errors = list(schema.iter_errors(e, data))

    assert len(errors) == 2


def test_iter_errors_requiredfieldinvalid():
    """Test iter_errors with a required field."""
    data = {'a': 1}
    test_schema = voluptuous.Schema({'a': int, 'b': str}, required=True)
    try:
        test_schema(data)
    except schema.MultipleInvalid as e:
        error = next(schema.iter_errors(e, data))

    assert isinstance(error.error, voluptuous.RequiredFieldInvalid)
    assert error.message == str(error.error)
    assert error.value is None


def test_iter_errors_typeinvalid():
    """Test iter_errors with an invalid type."""
    data = {'a': '1'}
    test_schema = voluptuous.Schema({'a': int})
    try:
        test_schema(data)
    except schema.MultipleInvalid as e:
        error = next(schema.iter_errors(e, data))

    assert isinstance(error.error, schema.TypeInvalid)
    assert error.message.endswith('got str')
    assert error.value == '1'


def test_missing_track_usage_rules():
    """Test that missing track usage rules doesn't validate."""
    doc = load_json('invalid-track-usage-rules.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_no_track_bundle_amwkey():
    """Test that a missing track bundle amwkey doesn't validate."""
    doc = load_json('invalid-track-bundle-amwkey.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_no_track_bundle_provider():
    """Test that a missing track bundle provider doesn't validate."""
    doc = load_json('invalid-track-bundle-provider.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_no_track_bundle_title():
    """Test that a missing track bundle title doesn't validate."""
    doc = load_json('invalid-track-bundle-title.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_no_track_isrc():
    """Test that a missing track ISRC doesn't validate."""
    doc = load_json('invalid-track-isrc.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


def test_valid():
    """Test a valid document."""
    doc = load_json('valid.json')
    assert schema.track_bundle(doc) == doc
