"""Schemas that can be used for validating common data types."""

# NOTE: The docstrings immediately following each schema are provided
# solely for Sphinx's autodoc. They are not useful Python docstrings and
# cannot be consumed by help() or a REPL.

from collections import namedtuple
import dateutil.parser
from functools import partial

from henson.exceptions import Abort
from voluptuous import (
    Any,
    Invalid,
    MultipleInvalid,
    Optional,
    Schema,
    TypeInvalid,
)

__all__ = ('iter_errors', 'validate_schema')

SchemaAllRequired = partial(Schema, required=True)

COMMERCIAL_MODEL_TYPES = (
    'AdvertisementSupportedModel',
    'DeviceFeeModel',
    'PayAsYouGoModel',
    'RightsClaimModel',
    'SubscriptionModel'
)

USE_TYPES = (
    'ConditionalDownload',
    'iHeartCustom',
    'NonInteractiveStream',
    'OnDemandStream',
    'PermanentDownload'
)


ValidationError = namedtuple('ValidationError', 'error message value')
"""A wrapper around a validation error.

Args:
    error (voluptuous.Error): The validation error.
    message (str): A friendly error message. If provided, more
        information than the message associated with ``error``.
    value: The value that failed validation. This will only be provided
        when the object being validated contained the field.
"""


class CommercialModelTypeInvalid(Invalid):
    """The value is not a valid commercialModelType.

    .. versionadded: 1.1.0
    """


def CommercialModelType(value):  # NOQA: N802
    """Validate CommercialModelType.

    Args:
        value (str): The commercialModelType in the message.

    Returns:
        str: The same commercialModelType passed into the function.

    Raises:
        CommercialModelTypeInvalid: If the commercialModelTypes
            is not defined in COMMERCIAL_MODEL_TYPES.

    .. versionadded: 1.1.0

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
    """The value is not a valid useType.

    .. versionadded: 1.1.0
    """


def UseType(value):  # NOQA: N802
    """Validate useType.

    Args:
        value (list): The useTypes in the message.

    Returns:
        list: The same useTypes passed into the function.

    Raises:
        UseTypeInvalid: If one of the useTypes is not defined in
            ``USE_TYPES``.

    .. versionadded: 1.1.0

    """
    for v in value:
        if v not in USE_TYPES:
            raise UseTypeInvalid("Expected one of '{0}', got '{1}'.".format(
                "', '".join(USE_TYPES), v))
    return value


def OffsetAwareDatetime(value):  # NOQA: N802
    """Validate offset aware date time.

    Args:
        value (str): Date time.

    Returns:
        str: The same date time passed into the function.

    Raises:
        Invalid: If date time could not be parsed.

    .. versionadded: 1.1.0

    """
    try:
        dateutil.parser.parse(value)
        return value
    except (TypeError, ValueError, OverflowError):
        raise Invalid('Could not parse date string: {}'.format(value))


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
    Optional('artists'): [Any(
        None, Schema({
            'artist_name': str,
            'artist_role': str,
            'sequence_number': Any(None, int),
        }))],
    Optional('url'): Any(None, str),
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
    Optional('text'): Any(None, str),
    Optional('year'): Any(None, int),
})
"""Schema to validate a copyright.

Args:
    text (Optional(str)): The full copyright text.
    year (Optional[int]): The copyright year.
"""

# TODO: Given the number of fields that are optional, this should
# probably be split up into two separate schemas, one for audio files
# and one for images. They can inherit from media like track and
# track_bundle inherit from product.
media = SchemaAllRequired({
    Optional('bitrate'): Any(None, str),
    Optional('channel'): Any(None, int),
    Optional('codec'): Any(None, str),
    Optional('count'): Any(None, int),
    Optional('number'): Any(None, int,),
    Optional('sampleRate'): Any(None, str),
    'source': str,
})
"""Schema to validate media.

``count`` and ``number`` are more likely to be provided for images than
for audio files. ``bitrate``, ``channel``, ``codec``, and
``sampleRate`` are more likely for audio files.

Args:
    bitrate (Optional[str]): The bitrate of the media file.
    channel (Optional[int]): The channel of the media file.
    codec (Optional[str]): The codec of the media file.
    count (Optional[int]): The total number of media files.
    number (Optional[int]): The number of the media file.
    sampleRate (Optional[str]): The sample rate of the media file.
    source (str): The location of the media file.
"""

# provider-related schemas
sub_label = SchemaAllRequired({
    Optional('name'): Any(None, str),
    'countries': [str],
})
"""Schema to valid a sub label.

Args:
    name (Optional[str]): The sub label's name.
    countries (list): A list of countries.
"""

label = SchemaAllRequired({
    'name': str,
    'subLabels': [sub_label],
})
"""Schema to validate a label.

Args:
    name (str): The label's name.
    subLabels (list): A list of sub labels.
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
    'action': str,
    'commercialModelType': CommercialModelType,
    'licensee': str,
    Optional('price'): Any(None, str),
    'territoryCode': str,
    'useType': UseType,
    'validFrom': Any(None, OffsetAwareDatetime),
    'validThrough': Any(None, OffsetAwareDatetime),
})
"""Schema to validate an offer.

Args:
    commercialModelType (CommercialModelType): The commercial model
        between the label or aggregator and their retail partners.
    licensee (str): The licensee for the offer.
    price (Optional[str]): The price used in the territory.
    territoryCode (str): The country code representing the territory.
    useType (UseType): The types of usage that are allowed.
    validFrom (Union[str, None]): The start date of the item's validity
        in ISO-8601 format.
    validThrough (Union[str, None]): The end date of the item's validity
        in ISO-8601 format.
"""


# products
product = SchemaAllRequired({
    'action': 'upsert',
    'amwKey': str,
    'artist': artist,
    'copyright': copyright,
    'duration': str,
    'explicitLyrics': bool,
    Optional('genre'): Any(None, str),
    Optional('id'): Any(None, int),
    Optional('internalId'): Any(None, str),
    Optional('media'): Any(None, media),
    'name': str,
    Optional('offers'): [offer],
    'provider': provider,
    Optional('publisher'): Any(None, str),
    Optional('version'): Any(None, str),
})
"""Schema to validate a product.

Args:
    action (str): The action to be taken on the product specified by
        ``amwKey``. Must be ``'upsert'``.
    amwKey (str): The product's unique identifier.
    artist (artist): The product's artist.
    copyright (copyright): The product's copyright.
    duration (str): The product's duration in ISO-8601 format.
    explicitLyrics (bool): Whether the product contains explicit
        lyrics.
    genre (str): The product's genre.
    id (Optional(int)): The product's internal id in the Ingestion database.
    internalId (Optional[int]): The track's internal identifier.
    media (media): Media files associated with the product.
    name (str): The product's name.
    offers (list): A list of offers for the product.
    provider (provider): The product's provider.
    publisher (Optional[str]): The product's publisher.
    version (Optional[str]): The product's version.
"""

track_schema = product.schema.copy()
track_schema.update({
    Optional('alternativeName'): Any(None, str),
    Optional('genre'): Any(None, str),
    Optional('grid'): Any(None, str),
    'index': int,
    'isrcCode': str,
    Optional('isrcCodeRaw'): Any(None, str),
    'number': int,
    Optional('participants'): Any(None, [participant]),
    'volume': int,
})

track = SchemaAllRequired(track_schema)
"""Schema to validate a track.

This schema is an extension of the :data:`product` schema.

Args:
    alternativeName (Optional[str]): The track's extended name.
    grid (Optional[str]): The track's Global Release Identifier.
    index (int): The track's index on the track bundle. This is often,
        but not always, based on the ``number``.
    isrcCode (str): The track's International Standard Recording Code.
    isrcCodeRaw (Optional(str)): The raw version of the track's
        International Standard Recording Code.
    number (int): The track's number on the track bundle.
    volume (int): The number of the track bundle's volumes on which the
        track appears.
"""

track_bundle_schema = product.schema.copy()
track_bundle_schema.update({
    'albumReleaseType': str,
    Optional('catalogNumber'): Any(None, str),
    Optional('ean'): Any(None, str),
    Optional('grid'): Any(None, str),
    Optional('icpn'): Any(None, str),
    'numTracks': int,
    'numVolumes': int,
    Optional('productCode'): Any(None, str),
    'releasedEvent': OffsetAwareDatetime,
    'tracks': [track],
    'upc': str,
    Optional('upcRaw'): Any(None, str),
})

track_bundle = SchemaAllRequired(track_bundle_schema)
"""Schema to validate a track bundle.

This schema is an extension of the :data:`product` schema.

Args:
    albumReleaseType (str): The product type.
    catalogNumber (Optional[str]): The track bundle's catalog number.
    ean (Optional[str]): The track bundle's International Article
        Number.
    grid (Optional[str]): The track bundle's Global Release Identifier.
    icpn (Optional[str]): The track bundle's International Code Product
        Number.
    numTracks (int): The number of tracks.
    numVolumes (int): The number of volumes that make up the
        track bundle.
    productCode (Optional[str]): The track bundle's product code.
    releasedEvent (Date): The product's release date.
    tracks (list): A list of tracks.
    upc (str): The track bundle's Universal Product Code.
    upcRaw (Optional(str)): The raw version of the track bundle's
        Universal Product Code.
"""

takedown = SchemaAllRequired({
    'action': 'takedown',
    'amwKey': str,
}, extra=True)
"""Schema to validate a product takedown.

Args:
    action (str): The action to be taken on the product specified by
        ``amwKey``. Must be ``'takedown'``.
    amwKey (str): The product's amwKey.
"""

purge = SchemaAllRequired({
    'action': 'purge',
    'grid': str,
    'icpn': str,
}, extra=True)
"""Schema to validate a product purge.

Args:
    action (str): Must be 'purge', indicates which action persist should take.
    grid (str): the GRiD for the product to be purged.
    icpn (str): the ICPN for the product to be purged.
"""

delivery = Any(track_bundle, takedown, purge)
"""Schema to validate a partner delivery.

Content must match the schema of either ``takedown`` or
``track_bundle``.
"""


del track_schema
del track_bundle_schema
