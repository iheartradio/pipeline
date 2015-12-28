"""Test ignore_provider."""

import pytest

from henson.exceptions import Abort
from pipeline import ignore_provider

TEST_PROVIDER = 'testing'
TEST_MESSAGE = {'provider': TEST_PROVIDER}


@pytest.mark.asyncio
async def test_empty_lists(test_app):
    """Test ignore_provider with empty lists of providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = []
    test_app.settings['EXCLUDED_PROVIDERS'] = []

    actual = await ignore_provider(test_app, TEST_MESSAGE)
    assert actual


@pytest.mark.asyncio
async def test_excluded(test_app):
    """Test ignore_provider with excluded providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = []
    test_app.settings['EXCLUDED_PROVIDERS'] = [TEST_PROVIDER + '1']

    actual = await ignore_provider(test_app, TEST_MESSAGE)
    assert actual


@pytest.mark.asyncio
async def test_excluded_ignore(test_app):
    """Test ignore_provider ignores with excluded providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = []
    test_app.settings['EXCLUDED_PROVIDERS'] = [TEST_PROVIDER]

    with pytest.raises(Abort):
        await ignore_provider(test_app, TEST_MESSAGE)


@pytest.mark.asyncio
async def test_included(test_app):
    """Test ignore_provider with included providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = [TEST_PROVIDER]
    test_app.settings['EXCLUDED_PROVIDERS'] = []

    actual = await ignore_provider(test_app, TEST_MESSAGE)
    assert actual


@pytest.mark.asyncio
async def test_included_ignore(test_app):
    """Test ignore_provider ignores with included providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = [TEST_PROVIDER + '1']
    test_app.settings['EXCLUDED_PROVIDERS'] = []

    with pytest.raises(Abort):
        await ignore_provider(test_app, TEST_MESSAGE)


@pytest.mark.asyncio
async def test_included_and_excluded(test_app):
    """Test ignore_provider with included and excluded providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = [TEST_PROVIDER]
    test_app.settings['EXCLUDED_PROVIDERS'] = [TEST_PROVIDER]

    actual = await ignore_provider(test_app, TEST_MESSAGE)
    assert actual


@pytest.mark.asyncio
async def test_no_providers(test_app):
    """Test ignore_provider with no providers."""
    test_app.settings.pop('INCLUDED_PROVIDERS', None)
    test_app.settings.pop('EXCLUDED_PROVIDERS', None)

    actual = await ignore_provider(test_app, TEST_MESSAGE)
    assert actual


@pytest.mark.asyncio
async def test_none(test_app):
    """Test ignore_provider with none providers."""
    test_app.settings['INCLUDED_PROVIDERS'] = None
    test_app.settings['EXCLUDED_PROVIDERS'] = None

    actual = await ignore_provider(test_app, TEST_MESSAGE)
    assert actual
