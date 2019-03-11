from mongoengine import *
from django.core.validators import MinLengthValidator
import uuid


class UserProfile(Document):
    name = StringField(required=True, validators=[MinLengthValidator(3)])
    google_email = EmailField(required=True, unique=True)
    google_picture = URLField()
    token = UUIDField(default=uuid.uuid4)
    is_active = BooleanField(default=True)

    @classmethod
    def create_from_google_info(cls, info):
        obj = cls(
            name=info["name"],
            google_picture=info["picture"],
            google_email=info["email"],
        )
        obj.save()
        return obj

    def update_with_google_info(self, info):
        self.name = info["name"]
        self.google_picture = info["picture"]
        self.google_email = info["email"]
        self.save()

    @staticmethod
    def is_authenticated():
        return True
