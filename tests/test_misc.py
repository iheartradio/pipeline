"""Miscellaneous tests."""

import pytest

import pipeline


@pytest.mark.parametrize('isrc, expected', (
    ('12-345-67-89012', '123456789012'),
    ('21-098-76-54321', '210987654321'),
))
def test_normalize_isrc(isrc, expected):
    """Test that ISRCs with dashes are transformed."""
    actual = pipeline.normalize_isrc(isrc)
    assert actual == expected


@pytest.mark.parametrize('isrc', (
    '123456789012',
    '210987654321',
))
def test_normalize_isrc_unchanged(isrc):
    """Test that ISRCs without dashes are unchanged."""
    assert isrc == pipeline.normalize_isrc(isrc)


@pytest.mark.parametrize('isrc, expected', (
    ('qm-9k-3120-0284', 'QM9K31200284'),
    ('qm9k31200284', 'QM9K31200284'),
))
def test_upper_cased_normalize_isrc(isrc, expected):
    """Test that ISRCs with dashes are transformed."""
    actual = pipeline.normalize_isrc(isrc)
    assert actual == expected


@pytest.mark.parametrize('upc, expected', (
    ('00616892587125', '616892587125'),
    ('00076743106828', '076743106828'),
    ('00044003728271', '044003728271'),
    ('00802097028420', '802097028420'),
    ('00061528101723', '061528101723'),
    ('00619061375226', '619061375226'),
    ('00044003727151', '044003727151'),
    ('00035561301228', '035561301228'),
    ('00803467000923', '803467000923'),
    ('00619061218523', '619061218523'),
    ('00856811001800', '856811001800'),
    ('00823674300234', '823674300234'),
    ('00775020927629', '775020927629'),
    ('00044003723795', '044003723795'),
    ('00821826000162', '821826000162'),
    ('00619061368020', '619061368020'),
    ('00053361303525', '053361303525'),
    ('00805386002729', '805386002729'),
    ('00053361309428', '053361309428'),
    ('00856811001794', '856811001794'),
))
def test_normalize_upc_leading_zeros(upc, expected):
    """Test that UPCs with leading zeros are transformed."""
    actual = pipeline.normalize_upc(upc)
    assert actual == expected


@pytest.mark.parametrize('upc', (
    '80330753510997',
    '80330753513226',
    '80330753510362',
    '80330753510447',
    '80330753510317',
    '80330753510355',
    '80330753510300',
    '80330753510430',
    '80330753510324',
    '80330753510348',
    '80330753511376',
    '80330753510539',
    '80330753510157',
    '80330753510423',
    '80330753510607',
    '80330753510461',
    '80330753510577',
    '80330753510188',
    '80330753510393',
    '80330753510560',
))
def test_normalize_upc_too_long_unchanged(upc):
    """Test that UPCs that are too long are unchanged."""
    assert upc == pipeline.normalize_upc(upc)


@pytest.mark.parametrize('upc', (
    '018736260971',
    '616822105825',
    '889845354086',
    '111118824126',
    '634479093388',
    '889176232091',
    '859715025446',
    '702730622643',
    '800684021212',
    '811868219042',
    '785688016726',
    '889845213406',
    '859712876850',
    '885767949478',
    '775957086963',
    '803057002429',
    '811868646121',
    '829410132374',
    '887516926396',
    '642738977492',
))
def test_normalize_upc_valid_unchanged(upc):
    """Test that valid UPCs are unchanged."""
    assert upc == pipeline.normalize_upc(upc)
