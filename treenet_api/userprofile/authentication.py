from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework import exceptions
from userprofile.models import UserProfile


class TokenAuthentication(BaseTokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            user = UserProfile.objects.get(token=key)
        except UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return user, user["token"]
