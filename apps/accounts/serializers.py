"""
Serializers for user registration and profile representation.

RegisterSerializer deliberately ignores any client-supplied `role`
value — see Phase 4 Architecture Discussion (section 2.3) for why
self-registration is restricted to the citizen role only.
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import Role, User


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of a user, used in nested responses."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "role", "date_joined"]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles citizen self-registration.

    Password is write-only and validated using Django's built-in
    password validators (configured in config/settings.py). Role is
    not accepted as input; it is always set to CITIZEN server-side.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password", "password_confirm"]

    def validate(self, attrs: dict) -> dict:
        """Ensure the two password fields match before object creation."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data: dict) -> User:
        """
        Create the user with role hardcoded to CITIZEN, regardless of
        what (if anything) was submitted in the request body.
        """
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(role=Role.CITIZEN, **validated_data)
        user.set_password(password)
        user.save()
        return user