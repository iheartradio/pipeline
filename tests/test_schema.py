"""Test the schemas."""

import copy
import json
import os

from henson.exceptions import Abort
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


@pytest.mark.parametrize('type_', (
    'AdvertisementSupportedModel',
    'DeviceFeeModel',
    'PayAsYouGoModel',
    'RightsClaimModel',
    'SubscriptionModel',
))
def test_commercialmodeltype(type_):
    """Test that a type is a CommercialModelType."""
    assert schema.CommercialModelType(type_) == type_


def test_empty_document():
    """Test that an empty document doesn't validate."""
    doc = load_json('empty.json')
    with pytest.raises(schema.MultipleInvalid):
        schema.track_bundle(doc)


@pytest.mark.parametrize('message', (
    {},
    {'action': 'takedown'},
    {'amw_key': '123'},
    {'action': 'upsert', 'amw_key': '123'},
))
def test_invalid_takedown(message):
    """Test invalid takedown delivery."""
    with pytest.raises(Abort):
        schema.validate_schema(schema.takedown, message)


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


def test_minimal_takendown():
    """Test that a valid minimal takedown passes validation."""
    expected = {'action': 'takedown', 'amw_key': '123'}
    actual = schema.validate_schema(schema.takedown, expected)
    assert actual == expected


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


@pytest.mark.parametrize('type_', (
    'testing',
    'invalidvalue',
    'this should fail',
    '123',
    '$5',
))
def test_raises_commercialmodeltypeinvalid(type_):
    """Test that invalid commercial models raise CommercialModelTypeInvalid."""
    assert type_ not in schema.COMMERCIAL_MODEL_TYPES
    with pytest.raises(schema.CommercialModelTypeInvalid):
        assert schema.CommercialModelType(type_) == type_


@pytest.mark.parametrize('type_', (
    ['testing1', 'testing2'],
    ['this should fail'],
    ['fail1', 'fail2', 'fail3'],
    ['invalid'],
))
def test_raises_usetypeinvalid(type_):
    """Test that invalid use types raise UseTypeInvalid."""
    assert type_ not in schema.USE_TYPES
    with pytest.raises(schema.UseTypeInvalid):
        assert schema.UseType(type_) == type_


def test_takedown():
    """Test that a valid takedown passes validation."""
    expected = load_json('valid.json')
    expected['action'] = 'takedown'
    actual = schema.validate_schema(schema.takedown, expected)
    assert actual == expected


def test_valid():
    """Test a valid document."""
    doc = load_json('valid.json')
    assert schema.track_bundle(doc) == doc


def test_upsert():
    """Test the upsert schema."""
    expected = load_json('valid.json')
    actual = schema.validate_schema(schema.delivery, expected)
    assert actual == expected


@pytest.mark.parametrize('type_', (
    ['ConditionalDownload'],
    ['NonInteractiveStream'],
    ['OnDemandStream'],
    ['PermanentDownload'],
))
def test_usetype(type_):
    """Test that a type is a UseType."""
    assert schema.UseType(type_) == type_


@pytest.mark.parametrize('schema_, expected', (
    (voluptuous.Schema(str), 'a'),
    (voluptuous.Schema([int]), [1, 2]),
    (
        voluptuous.Schema({'a': int}, extra=voluptuous.ALLOW_EXTRA),
        {'a': 1, 'b': 'c'}
    ),
))
def test_validate_message(schema_, expected):
    """Test a message that validates its schema."""
    actual = schema.validate_schema(schema_, expected)
    assert actual == expected


@pytest.mark.parametrize('schema_, message', (
    (voluptuous.Schema(str), 1),
    (voluptuous.Schema([int]), [1, 'a']),
    (voluptuous.Schema({'a': int}), {'a': 1, 'b': 2}),
))
def test_validate_message_invalid(schema_, message):
    """Test that invalid messages fail to validate."""
    with pytest.raises(Abort):
        schema.validate_schema(schema_, message)
