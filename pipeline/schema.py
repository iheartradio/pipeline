"""Schemas that can be used for validating common data types."""

# NOTE: The docstrings immediately following each schema are provided
# solely for Sphinx's autodoc. They are not useful Python docstrings and
# cannot be consumed by help() or a REPL.

from collections import namedtuple
from functools import partial

# Import multipleInvalid to expose it through the module.
from voluptuous import MultipleInvalid, Optional, Schema, truth, TypeInvalid  # NOQA

SchemaAllRequired = partial(Schema, required=True)

VALID_ACTIONS = ('upsert', 'takedown')


ValidationError = namedtuple('ValidationError', 'error message value')
"""A wrapper around a validation error.

Args:
    error (voluptuous.Error): The validation error.
    message (str): A friendly error message. If provided, more
        information than the message associated with ``error``.
    value: The value that failed validation. This will only be provided
        when the object being validated contained the field.

.. versionadded:: 0.2.0
"""


@truth
def _is_valid_action(action):
    """Return if an action is valid.

    Args:
        action (str): The action to validate.

    Returns:
        bool: Whether the action is valid.
    """
    return action.lower() in VALID_ACTIONS


def iter_errors(exc, data):
    """Return a generator containing validation errors.

    Args:
        exc (voluptuous.MultipleInvalid): The exception raised when
            validating against a schema.
        data (dict): The document being validated.

    Yields:
        ValidationError: The error.

    .. versionadded:: 0.2.0
    """
    # Get a copy of the original value so data can be reset in the loop.
    original = data

    # Loop through all the errors and yield the error message and the
    # value to which it refers.
    for error in exc.errors:
        data = None
        if isinstance(error, TypeInvalid):
            data = original

            # voluptuous provides a path of keys and indexes that can be
            # used to retrieve the value.
            for key_or_index in error.path:
                data = data.__getitem__(key_or_index)

            msg = '{}, got {}'.format(error, type(data).__name__)
        else:
            msg = str(error)

        yield ValidationError(error, msg, data)


# shared sub-types
artist = SchemaAllRequired({
    'name': str,
    Optional('url'): str,
})
"""Schema to validate an artist.

Args:
    name (str): The artist's name.
    url (Optional[str]): The artist's URL.
"""

participant = SchemaAllRequired({
    'name': str,
    'role': str,
})
"""Schema to validate a participant.

Args:
    name (str): The participant's name.
    role (str): The participant's role on the track.
"""

copyright = SchemaAllRequired({
    'text': str,
    Optional('year'): int,
})
"""Schema to validate a copyright.

Args:
    text (str): The full copyright text.
    year (Optional[int]): The copyright year.
"""

media = SchemaAllRequired({
    Optional('count'): int,
    Optional('number'): int,
    'source': str,
})
"""Schema to validate media.

``count`` and ``number`` are more likely to be provided for images than
for audio files.

Args:
    source (str): The location of the media file.
    count (Optional[int]): The total number of media files.
    number (Optional[int]): The number of the media file.
"""

physical_product = SchemaAllRequired({
    'artist': str,
    'name': str,
    'upc': str,
})
"""Schema to validate a physical product.

Args:
    artist (str): The name of the product's artist.
    name (str): The product's name.
    upc (str): The product's Universal Product Code.
"""

release = SchemaAllRequired({
    'date': str,
    'year': int,
})
"""Schema to validate a release date.

Args:
    date (str): The release date.
    year (int): The release year.
"""


# provider-related schemas
sub_label = SchemaAllRequired({
    'name': str,
    'countries': [str],
})
"""Schema to valid a sub label.

Args:
    name (str): The sub label's name.
    countries (list): A list of countries.
"""

label = SchemaAllRequired({
    'name': str,
    'sub_labels': [sub_label],
})
"""Schema to validate a label.

Args:
    name (str): The label's name.
    sub_labels (list): A list of sub labels.
"""

provider = SchemaAllRequired({
    'name': str,
    'labels': [label],
})
"""Schema to validate a provider.

Args:
    name (str): The provider's name.
    labels (list): A list of labels.
"""


sales_territory = SchemaAllRequired({
    'country_code': str,
    Optional('price_code'): str,
    'sales_start_date': str,
    Optional('sales_end_date'): str,
})
"""Schema to validate a sales territory.


Args:
    country_code (str): The country code representing the territory.
    price_code (Optional[str]): The price code used in the territory.
    sales_start_date (str): The date of availability in the territory.
    sales_end_date (Optional[str]): The date of the end of availability
        in the territory.
"""


usage_rules = SchemaAllRequired({
    'allow_bundle': bool,
    'allow_burn_play_on_pc': bool,
    'allow_burn_to_cd': bool,
    'allow_mobile': bool,
    'allow_permanent': bool,
    'allow_promotional': bool,
    'allow_streaming': bool,
    'allow_subscription': bool,
    'allow_transfer_to_nsdmi': bool,
    'allow_transfer_to_sdmi': bool,
    'allow_unbundle': bool,
    'delete_on_clock_rollback': bool,
    'disable_on_clock_rollback': bool,
    'drm_free': bool,
    'limited': bool,
})
"""Schema to validate usage rules.

Args:
    allow_bundle (bool): The allowbundle usage rule.
    allow_burn_play_on_pc (bool): The allowburnplayonpc usage rule.
    allow_burn_to_cd (bool): The allowburntocd usage rule.
    allow_mobile (bool): The allowmobile usage rule.
    allow_permanent (bool): The allowpermanent usage rule.
    allow_promotional (bool): The allowpromotional usage rule.
    allow_streaming (bool): The allowstreaming usage rule.
    allow_subscription (bool): The allowsubscription usage rule.
    allow_transfer_to_nsdmi (bool): The allowtransfertonsdmi usage rule.
    allow_transfer_to_sdmi (bool): The allowtransfertosdmi usage rule.
    allow_unbundle (bool): The allowunbundle usage rule.
    delete_on_clock_rollback (bool): The deleteonclockrollback usage
        rule.
    disable_on_clock_rollback (bool): The disableonclockrollback usage
        rule.
    drm_free (bool): The drmfree usage rule.
    limited (bool): The limited usage rule.
"""


# products
product = SchemaAllRequired({
    'action': _is_valid_action,
    'amw_key': str,
    'artist': artist,
    'copyright': copyright,
    Optional('duration'): int,
    'explicit_lyrics': bool,
    'genre': str,
    'media': media,
    'provider': provider,
    Optional('publisher'): str,
    'sales_territories': [sales_territory],
    'title': str,
    'usage_rules': usage_rules,
    Optional('version'): str,
})
"""Schema to validate a product.

Args:
    action (str): The action to perform on the product, should be one of
        ``upsert`` or ``takedown``.
    amw_key (str): The product's unique identifier.
    artist (artist): The product's artist.
    copyright (copyright): The product's copyright.
    duration (Optional[int]): The product's duration.
    explicit_lyrics (bool): Whether the product contains explicit
        lyrics.
    genre (str): The product's genre.
    media (media): Media files associated with the product.
    provider (provider): The product's provider.
    publisher (Optional[str]): The product's publisher.
    sales_territories (list): A list of sales territories for the
        product.
    title (str): The product's title.
    usage_rules (usage_rules): The product's usage rules.
    version (Optional[str]): The product's version.
"""

track_schema = product.schema.copy()
track_schema.update({
    'genre': str,
    'index': int,
    Optional('internal_id'): str,
    'isrc': str,
    'number': int,
    Optional('participants'): [participant],
    Optional('title_extended'): str,
    'volume': int,
    Optional('windows_drm_id'): str,
})

track = SchemaAllRequired(track_schema)
"""Schema to validate a track.

This schema is an extension of the :data:`product` schema.

Args:
    index (int): The track's index on the track bundle. This is often,
        but not always, based on the ``number``.
    internal_id (Optional[int]): The track's internal identifier.
    isrc (str): The track's International Standard Recording Code.
    number (int): The track's number on the track bundle.
    title_extended (Optional[str]): The track's extended title.
    volume (int): The number of the track bundle's volumes on which the
        track appears.
    windows_drm_id (Optional[str]): The track's Windows DRM ID.
"""

track_bundle_schema = product.schema.copy()
track_bundle_schema.update({
    Optional('catalog_number'): str,
    Optional('ean'): str,
    Optional('grid'): str,
    Optional('icpn'): str,
    'internal_id': str,
    Optional('physical'): physical_product,
    Optional('product_code'): str,
    'release': release,
    'track_count': int,
    'tracks': [track],
    'type': str,
    'upc': str,
    'volume_count': int,
})

track_bundle = SchemaAllRequired(track_bundle_schema)
"""Schema to validate a track bundle.

This schema is an extension of the :data:`product` schema.

Args:
    catalog_number (Optional[str]): The track bundle's catalog number.
    ean (Optional[str]): The track bundle's International Article
        Number.
    grid (Optional[str]): The track bundle's Global Release Identifier.
    icpn (Optional[str]): The track bundle's International Code Product
        Number.
    internal_id (Optional[int]): The track bundle's internal identifier.
    physical: (Optional[physical_product]): The track bundle's physical
        representation.
    product_code (Optional[str]): The track bundle's product code.
    release (release): The product's release date.
    track_count (int): The number of tracks.
    tracks (list): A list of tracks.
    type (str): The product type.
    upc (str): The track bundle's Universal Product Code.
    volume_count (int): The number of volumes that make up the track bundle.
"""

del track_schema
del track_bundle_schema
