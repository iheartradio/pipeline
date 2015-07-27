"""Test ignore_provider."""

from pipeline import ignore_provider

TEST_PROVIDER = 'testing'


def test_empty_lists():
    """Test ignore_provider with empty lists of providers."""
    assert not ignore_provider(TEST_PROVIDER, included=[], excluded=[])


def test_excluded():
    """Test ignore_provider with excluded providers."""
    assert not ignore_provider(
        TEST_PROVIDER, included=[], excluded=[TEST_PROVIDER + '1'])


def test_excluded_ignore():
    """Test ignore_provider ignores with excluded providers."""
    assert ignore_provider(
        TEST_PROVIDER, included=[], excluded=[TEST_PROVIDER])


def test_included():
    """Test ignore_provider with included providers."""
    assert not ignore_provider(
        TEST_PROVIDER, included=[TEST_PROVIDER], excluded=[])


def test_included_ignore():
    """Test ignore_provider ignores with included providers."""
    assert ignore_provider(
        TEST_PROVIDER, included=[TEST_PROVIDER + '1'], excluded=[])


def test_included_and_excluded():
    """Test ignore_provider with included and excluded providers."""
    assert not ignore_provider(
        TEST_PROVIDER, included=[TEST_PROVIDER], excluded=[TEST_PROVIDER])


def test_none():
    """Test ignore_provider with no providers."""
    assert not ignore_provider(TEST_PROVIDER, included=None, excluded=None)
