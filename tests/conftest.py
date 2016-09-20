"""Test configuration."""

import pytest


class Application:
    """A stub application that can be used for testing.

    Args:
        **settings: Keyword arguments that will be used as settings.
    """

    def __init__(self, **settings):
        """Initialize the instance."""
        self.name = 'testing'
        self.settings = settings


class Producer:
    """A stub producer that can be used for testing.

    Args:
        app: The application for which this producer produces.
    """

    def __init__(self, app):
        """Initialize the instance."""
        self.app = app
        self.sent_error = None
        self.sent_message = None

    async def error(self, message):
        """Mock send an error message."""
        self.sent_error = message

    async def send(self, message, *, routing_key=None):
        """Mock send a message."""
        self.sent_message = message
        self.routing_key = routing_key


@pytest.fixture
def test_app():
    """Return a test application."""
    app = Application()
    return app


@pytest.fixture
def test_producer(test_app):
    """Return a test producer."""
    return Producer(test_app)
