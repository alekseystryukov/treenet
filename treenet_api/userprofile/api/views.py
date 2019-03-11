from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from userprofile.models import UserProfile
from userprofile.api.serializers import UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from urllib import urlencode
import requests
import logging
import yaml

logger = logging.getLogger("api.user_profile")

BASE_URL = 'https://accounts.google.com/o/oauth2/'
AUTH_URL = BASE_URL + 'auth'
TOKEN_URL = BASE_URL + 'token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

with open("userprofile/google_keys.yaml") as f:
    google_data = yaml.load(f)

GOOGLE_CLIENT_ID = google_data.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = google_data.get("GOOGLE_CLIENT_SECRET")

REDIRECT_URI = ''

# AUTH_PARAMS = {
#     "response_type": "code",
#     "client_id": GOOGLE_CLIENT_ID,
#     "redirect_uri": REDIRECT_URI,
#     "scope": "https://www.googleapis.com/auth/userinfo.profile "
#              "https://www.googleapis.com/auth/userinfo.email"
# }

TOKEN_PARAMS = {
    "client_id": GOOGLE_CLIENT_ID,
    "client_secret": GOOGLE_CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}


def get_access_token(code):
    params = dict(**TOKEN_PARAMS)
    params["code"] = code
    content_length = len(urlencode(params))
    params['content-length'] = str(content_length)
    r = requests.post(TOKEN_URL, data=params)
    data = r.json()
    logger.info(str(data))
    return data["access_token"]


def get_user_info(code):
    access_token = get_access_token(code)
    headers = {"Authorization": "OAuth %s" % access_token}
    data = requests.get(USER_INFO_URL, headers=headers)
    return data.json()


class AuthView(APIView):

    @staticmethod
    def get(request):

        if isinstance(request.user, UserProfile):
            return Response(data=UserSerializer(request.user).data)

        # 2nd step of Oauth
        if 'code' in request.GET:
            code = request.GET.get('code')
            user_info = get_user_info(code)
            try:
                user = UserProfile.objects.get(google_email=user_info["email"])
            except UserProfile.DoesNotExist:
                user = UserProfile.create_from_google_info(user_info)
            else:
                user.update_with_google_info(user_info)
            return Response(data=UserSerializer(user).data)

        return Response({"client_id": GOOGLE_CLIENT_ID}, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    @permission_classes((IsAuthenticated,))
    def patch(request):
        user = request.user

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = UserSerializer(user).data
        return Response(data=data)
