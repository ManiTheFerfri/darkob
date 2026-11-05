"""Enumerations documented by the Rubika Bot API.

Every value here comes from the "models" page of the official reference
(<https://rubika.ir/botapi/models>). Each is a ``str`` enum, so an instance
serialises to the exact wire value::

    from darkob.bot.models import ButtonType, FileType

    ButtonType.Selection == "Selection"      # True
    FileType.Voice                           # "Voice"

Unknown future values are still accepted by the API; these enums exist so
you do not have to memorise spellings, not to lock the server down.
"""

from __future__ import annotations

from enum import Enum

__all__ = [
    "ButtonType",
    "ChatKeypadType",
    "ChatType",
    "FileType",
    "ForwardedFrom",
    "PaymentStatus",
    "PollStatus",
    "MessageSender",
    "ButtonSelectionType",
    "ButtonSelectionGet",
    "ButtonSelectionSearch",
    "ButtonCalendarType",
    "ButtonLocationType",
    "ButtonTextboxKeypad",
    "ButtonTextboxLine",
    "EventType",
    "EventJoinType",
]


class ButtonType(str, Enum):
    """``ButtonTypeEnum`` — what a keypad button does."""

    Simple = "Simple"
    Selection = "Selection"
    Calendar = "Calendar"
    NumberPicker = "NumberPicker"
    StringPicker = "StringPicker"
    Location = "Location"
    Payment = "Payment"
    CameraImage = "CameraImage"
    CameraVideo = "CameraVideo"
    GalleryImage = "GalleryImage"
    GalleryVideo = "GalleryVideo"
    File = "File"
    Audio = "Audio"
    RecordAudio = "RecordAudio"
    Textbox = "Textbox"
    Link = "Link"
    AskMyPhoneNumber = "AskMyPhoneNumber"
    AskMyLocation = "AskMyLocation"
    Barcode = "Barcode"


class ChatKeypadType(str, Enum):
    """``ChatKeypadTypeEnum`` — how a chat keypad update applies."""

    None_ = "None"
    New = "New"
    Remove = "Remove"


class ChatType(str, Enum):
    """``ChatTypeEnum``"""

    User = "User"
    Bot = "Bot"
    Group = "Group"
    Channel = "Channel"


class FileType(str, Enum):
    """``FileTypeEnum`` — accepted values for ``request_send_file``."""

    File = "File"
    Image = "Image"
    Voice = "Voice"
    Video = "Video"
    Music = "Music"
    Gif = "Gif"


class ForwardedFrom(str, Enum):
    """``ForwardedFromEnum``"""

    User = "User"
    Channel = "Channel"
    Bot = "Bot"


class PaymentStatus(str, Enum):
    """``PaymentStatusEnum``"""

    Paid = "Paid"
    NotPaid = "NotPaid"


class PollStatus(str, Enum):
    """``PollStatusEnum``"""

    Open = "Open"
    Closed = "Closed"


class MessageSender(str, Enum):
    """``MessageSenderEnum``"""

    User = "User"
    Bot = "Bot"


class ButtonSelectionType(str, Enum):
    """``ButtonSelectionTypeEnum`` — how selection items are rendered."""

    TextOnly = "TextOnly"
    TextImgThu = "TextImgThu"
    TextImgBig = "TextImgBig"


class ButtonSelectionGet(str, Enum):
    """``ButtonSelectionGetEnum`` — where selection items come from."""

    Local = "Local"
    Api = "Api"


class ButtonSelectionSearch(str, Enum):
    """``ButtonSelectionSearchEnum``"""

    None_ = "None"
    Local = "Local"
    Api = "Api"


class ButtonCalendarType(str, Enum):
    """``ButtonCalendarTypeEnum`` — Persian (Jalali) or Gregorian."""

    DatePersian = "DatePersian"
    DateGregorian = "DateGregorian"


class ButtonLocationType(str, Enum):
    """``ButtonLocationTypeEnum``"""

    Picker = "Picker"
    View = "View"


class ButtonTextboxKeypad(str, Enum):
    """``ButtonTextboxTypeKeypadEnum`` — keyboard shown for a textbox."""

    String = "String"
    Number = "Number"


class ButtonTextboxLine(str, Enum):
    """``ButtonTextboxTypeLineEnum``"""

    SingleLine = "SingleLine"
    MultiLine = "MultiLine"


class EventType(str, Enum):
    """``EventTypeEnum`` — system events a bot receives."""

    BotJoined = "BotJoined"
    BotRemoved = "BotRemoved"
    BotPermissionsChanged = "BotPermissionsChanged"


class EventJoinType(str, Enum):
    """``EventJoinTypeEnum``"""

    Member = "Member"
    Admin = "Admin"
