from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import darkob

class UpdateMyBio:
    async def update_my_bio(self: "darkob.Messenger", bio: str):
        """
        Update user's biography.

        Parameters:
            bio (str): The updated biography (max 150 characters).

        Returns:
            The updated user information.
        """
        from ...exceptions import InvalidInput

        if len(bio) > 150:
            raise InvalidInput("'bio' must be 150 characters or less.")

        input_data = {
            'bio': bio,
            'updated_parameters': ['bio']
        }

        return await self.request(method='updateProfile', input=input_data)