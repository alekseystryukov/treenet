from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.fields import SerializerMethodField
from userprofile.models import UserProfile


class UserSerializer(DocumentSerializer):
    picture = SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('name', 'token', 'picture')

    @staticmethod
    def get_picture(obj):
        return obj.google_picture


class UserUpdateSerializer(DocumentSerializer):

    class Meta:
        model = UserProfile
        fields = ('name',)
