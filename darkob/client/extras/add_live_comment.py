from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

_UNSET = object()


def _bind_live_arguments(args, live_id, access_token, comment):
    if len(args) > 3:
        raise TypeError("add_live_comment() accepts at most 3 positional arguments")

    # Only a numeric live ID followed by a GUID-shaped token proves upstream
    # order. Every other positional pair keeps the pre-1.18 convention.
    if (
        len(args) >= 2
        and isinstance(args[0], str)
        and args[0].isdigit()
        and isinstance(args[1], str)
        and args[1].startswith(("u0", "b0"))
    ):
        positional_names = ("live_id", "access_token", "comment")
    elif len(args) == 1 and access_token is not _UNSET and live_id is _UNSET:
        positional_names = ("live_id",)
    else:
        positional_names = ("access_token", "live_id", "comment")

    values = {
        "live_id": live_id,
        "access_token": access_token,
        "comment": comment,
    }
    for name, value in zip(positional_names, args):
        if values[name] is not _UNSET:
            raise TypeError(f"add_live_comment() got multiple values for '{name}'")
        values[name] = value

    missing = [name for name, value in values.items() if value is _UNSET]
    if missing:
        raise TypeError(
            "add_live_comment() missing required arguments: " + ", ".join(missing)
        )
    return values


class AddLiveComment:
    async def add_live_comment(
        self: "darkob.Messenger",
        *args,
        live_id: str = _UNSET,
        access_token: str = _UNSET,
        comment: str = _UNSET
    ):
        """Adds a comment to a live stream.

        Keyword arguments are canonical and unambiguous. Positional arguments
        accept both legacy ``(access_token, live_id, comment)`` and upstream
        ``(live_id, access_token, comment)``. Upstream order is selected only
        when the first argument is all digits and the second starts with
        ``u0`` or ``b0``; otherwise legacy order is retained, since arbitrary
        strings cannot always be distinguished reliably.

        Parameters:
            live_id (str): The ID of the live stream.
            access_token (str): The access token for authentication.
            comment (str): The text of the comment.

        Returns:
            The result of the API call.
        """
        values = _bind_live_arguments(args, live_id, access_token, comment)
        input_data = {
            'live_id': values['live_id'],
            'access_token': values['access_token'],
            'text': values['comment']
        }
        return await self.request(
            method='addLiveComment',
            input=input_data
        )
