"""Common utilities for the Ingestion Pipeline."""

__all__ = ('ignore_provider',)


def ignore_provider(provider, included=None, excluded=None):
    """Return whether a provider should be ignored.

    If ``included`` is not empty, this function will return ``False``
    for any provider in the list and ``True`` for all other providers.
    The provider will only be checked against ``excluded`` when
    ``included`` is empty.

    Args:
        provider (str): The identifier of the provider to check.
        included (list, optional): A list of all providers not to
          ignore.
        excluded (list, optional): A list of providers that should be
          ignored.

    Returns:
        bool: True if the provider should be ignored.
    """
    if included:
        # If there is a list of included providers, it is the only thing
        # checked to determine whether or not to ignore the provider.
        return provider not in included

    return provider in (excluded or ())
