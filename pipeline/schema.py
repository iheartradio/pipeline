"""Schemas that can be used for validating common data types."""

# NOTE: The docstrings immediately following each schema are provided
# solely for Sphinx's autodoc. They are not useful Python docstrings and
# cannot be consumed by help() or a REPL.

from collections import namedtuple
from functools import partial

from henson.exceptions import Abort
from voluptuous import (
    Any,
    Datetime,
    Invalid,
    MultipleInvalid,
    Optional,
    Schema,
    TypeInvalid,
)

__all__ = ('iter_errors', 'validate_schema')

SchemaAllRequired = partial(Schema, required=True)

COMMERCIAL_MODEL_TYPES = [
    'AdvertisementSupportedModel',
    'DeviceFeeModel',
    'PayAsYouGoModel',
    'RightsClaimModel',
    'SubscriptionModel'
]
USE_TYPES = [
    'ConditionalDownload',
    'NonInteractiveStream',
    'OnDemandStream',
    'PermanentDownload'
]


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


class CommercialModelTypeInvalid(Invalid):
    """The value is not a valid commercialModelType."""


def CommercialModelType(value):  # NOQA: N802
    """Validator for CommercialModelType.

    Args:
        value (str): The commercialModelType in the message.

    Returns:
        str: The same commercialModelType passed into the function.

    Raises:
        CommercialModelTypeInvalid: If the commercialModelTypes
            is not defined in COMMERCIAL_MODEL_TYPES.
    """
    if value not in COMMERCIAL_MODEL_TYPES:
        raise CommercialModelTypeInvalid(
            "Expected one of '{0}', got '{1}'.".format(
                "', '".join(COMMERCIAL_MODEL_TYPES), value))
    return value


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


class UseTypeInvalid(Invalid):
    """The value is not a valid useType."""


def UseType(value):  # NOQA: N802
    """Validator for useType.

    Args:
        value (list): The useTypes in the message.

    Returns:
        list: The same useTypes passed into the function.

    Raises:
        UseTypeInvalid: If one of the useTypes is not defined in USE_TYPES.
    """
    for v in value:
        if v not in USE_TYPES:
            raise UseTypeInvalid("Expected one of '{0}', got '{1}'.".format(
                "', '".join(USE_TYPES), v))
    return value


def validate_schema(schema, message, logger=None):
    """Validate a message against a schema.

    Args:
        schema (voluptuous.Schema): The schema against which to
            validate.
        message (dict): The message to validate.
        logger (Optional[logging.RootLogger]): An instance of a logger
            that, if provided, will be used to log the schema validation
            errors.

    Returns:
        dict: The validated message upon successful validation.

    .. versionadded:: 0.3.0
    """
    try:
        return schema(message)
    except MultipleInvalid as e:
        if logger is not None:
            logger.error(
                'schema.invalid', errors=list(iter_errors(e, data=message)))
        raise Abort('schema.invalid', message)


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

# TODO: Given the number of fields that are optional, this should
# probably be split up into two separate schemas, one for audio files
# and one for images. They can inherit from media like track and
# track_bundle inherit from product.
media = SchemaAllRequired({
    Optional('bitrate'): str,
    Optional('channel'): int,
    Optional('codec'): str,
    Optional('count'): int,
    Optional('number'): int,
    Optional('sample_rate'): str,
    'source': str,
})
"""Schema to validate media.

``count`` and ``number`` are more likely to be provided for images than
for audio files. ``bitrate``, ``channel``, ``codec``, and
``sample_rate`` are more likely for audio files.

Args:
    bitrate (Optional[str]): The bitrate of the media file.
    channel (Optional[int]): The channel of the media file.
    codec (Optional[str]): The codec of the media file.
    count (Optional[int]): The total number of media files.
    number (Optional[int]): The number of the media file.
    sample_rate (Optional[str]): The sample rate of the media file.
    source (str): The location of the media file.
"""

physical_product = SchemaAllRequired({
    'byArtist': str,
    'name': str,
    'upc': str,
})
"""Schema to validate a physical product.

Args:
    byArtist (str): The name of the product's artist.
    name (str): The product's name.
    upc (str): The product's Universal Product Code.
"""

# provider-related schemas
sub_label = SchemaAllRequired({
    Optional('name'): str,
    'countries': [str],
})
"""Schema to valid a sub label.

Args:
    name (Optional[str]): The sub label's name.
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

offer = SchemaAllRequired({
    'commercialModelType': CommercialModelType,
    'licensee': str,
    'preOrderPreviewDate': Datetime('%Y-%m-%d'),
    'preOrderReleaseDate': Datetime('%Y-%m-%d'),
    'territoryCode': str,
    Optional('price'): str,
    'useType': UseType,
    'validityPeriod': str,
})
"""Schema to validate an offer.

Args:
    commercialModelType (CommercialModelType): The commercial model
        between the label or aggregator and their retail partners.
    licensee (str): The licensee for the offer.
    preOrderPreviewDate (Date): The date for preorder preview.
    preOrderReleaseDate (Date): The date for preorder release.
    territoryCode (str): The country code representing the territory.
    price (Optional[str]): The price used in the territory.
    useType (UseType): The types of usage that are allowed.
    validityPeriod (str): The date range of availability in the territory.
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
    'action': 'upsert',
    'amw_key': str,
    'artist': artist,
    'copyright': copyright,
    'duration': str,
    'explicit_lyrics': bool,
    'genre': str,
    Optional('internal_id'): str,
    Optional('media'): media,
    'name': str,
    'offers': [offer],
    'provider': provider,
    Optional('publisher'): str,
    'usage_rules': usage_rules,
    Optional('version'): str,
})
"""Schema to validate a product.

Args:
    action (str): The action to be taken on the product specified by
        ``amw_key``. Must be ``'upsert'``.
    amw_key (str): The product's unique identifier.
    artist (artist): The product's artist.
    copyright (copyright): The product's copyright.
    duration (str): The product's duration in ISO-8601 format.
    explicit_lyrics (bool): Whether the product contains explicit
        lyrics.
    genre (str): The product's genre.
    internal_id (Optional[int]): The track's internal identifier.
    media (media): Media files associated with the product.
    name (str): The product's name.
    offers (list): A list of offers for the product.
    provider (provider): The product's provider.
    publisher (Optional[str]): The product's publisher.
    usage_rules (usage_rules): The product's usage rules.
    version (Optional[str]): The product's version.
"""

track_schema = product.schema.copy()
track_schema.update({
    Optional('alternativeName'): str,
    'genre': str,
    'index': int,
    'isrcCode': str,
    'number': int,
    Optional('participants'): [participant],
    'volume': int,
})

track = SchemaAllRequired(track_schema)
"""Schema to validate a track.

This schema is an extension of the :data:`product` schema.

Args:
    alternativeName (Optional[str]): The track's extended name.
    index (int): The track's index on the track bundle. This is often,
        but not always, based on the ``number``.
    isrcCode (str): The track's International Standard Recording Code.
    number (int): The track's number on the track bundle.
    volume (int): The number of the track bundle's volumes on which the
        track appears.
"""

track_bundle_schema = product.schema.copy()
track_bundle_schema.update({
    'albumReleaseType': str,
    Optional('catalog_number'): str,
    Optional('ean'): str,
    Optional('grid'): str,
    Optional('icpn'): str,
    'numTracks': int,
    'numVolumes': int,
    Optional('physical'): physical_product,
    Optional('product_code'): str,
    'releasedEvent': Datetime('%Y-%m-%d'),
    'tracks': [track],
    'upc': str,
})

track_bundle = SchemaAllRequired(track_bundle_schema)
"""Schema to validate a track bundle.

This schema is an extension of the :data:`product` schema.

Args:
    albumReleaseType (str): The product type.
    catalog_number (Optional[str]): The track bundle's catalog number.
    ean (Optional[str]): The track bundle's International Article
        Number.
    grid (Optional[str]): The track bundle's Global Release Identifier.
    icpn (Optional[str]): The track bundle's International Code Product
        Number.
    numTracks (int): The number of tracks.
    numVolumes (int): The number of volumes that make up the
        track bundle.
    physical: (Optional[physical_product]): The track bundle's physical
        representation.
    product_code (Optional[str]): The track bundle's product code.
    releasedEvent (Date): The product's release date.
    tracks (list): A list of tracks.
    upc (str): The track bundle's Universal Product Code.
"""

takedown = SchemaAllRequired({
    'action': 'takedown',
    'amw_key': str,
}, extra=True)
"""Schema to validate a product takedown.

Args:
    action (str): The action to be taken on the product specified by
        ``amw_key``. Must be ``'takedown'``.
    amw_key (str): The product's amw_key.
"""

delivery = Any(track_bundle, takedown)
"""Schema to validate a partner delivery.

Content must match the schema of either ``takedown`` or ``track_bundle``.
"""


del track_schema
del track_bundle_schema
