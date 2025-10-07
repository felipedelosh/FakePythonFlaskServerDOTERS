# app/models/User.py
from typing import Optional

class User:
    def __init__(
        self,
        language: str,
        enrollingSponsor: str,
        enrollingChannel: str,
        phoneNumber: str,
        email: str,
        password: str,
        activationUrl: str,
        subscribeToNotifications: bool,
        firstName: str,
        lastName: str,
        title: Optional[str] = None,
        dateOfBirth: Optional[str] = None,
        gender: str = "XX",
        residentCountry: str = "MX",
    ):
        self.language = language
        self.enrollingSponsor = enrollingSponsor
        self.enrollingChannel = enrollingChannel
        self.phoneNumber = phoneNumber
        self.email = email
        self.password = password
        self.activationUrl = activationUrl
        self.subscribeToNotifications = subscribeToNotifications
        self.firstName = firstName
        self.lastName = lastName
        self.title = title
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.residentCountry = residentCountry

    @classmethod
    def from_payload(cls, payload: dict):
        """Crea un objeto User a partir del JSON anidado del request."""
        loyalty = payload.get("loyaltyDetails", {})
        personal = payload.get("personalDetails", {})
        name = personal.get("name", {})

        return cls(
            language=payload.get("language", "es-MX"),
            enrollingSponsor=loyalty.get("enrollingSponsor", ""),
            enrollingChannel=loyalty.get("enrollingChannel", ""),
            phoneNumber=payload.get("phoneNumber", ""),
            email=payload.get("email", ""),
            password=payload.get("password", ""),
            activationUrl=payload.get("activationUrl", ""),
            subscribeToNotifications=payload.get("subscribeToNotifications", True),
            firstName=name.get("firstName", ""),
            lastName=name.get("lastName", ""),
            title=name.get("title"),
            dateOfBirth=personal.get("dateOfBirth"),
            gender=personal.get("gender", "XX"),
            residentCountry=personal.get("residentCountry", "MX"),
        )

    def __repr__(self):
        return f"<User {self.email}>"
