import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from InnotterUser.models import User


def expired_token(request):
    refresh_token = request.COOKIES['refresh_token']

    try:
        jwt.decode(refresh_token, settings.SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        msg = 'Authentication error. Expired access and refresh token.'
        raise exceptions.AuthenticationFailed(msg)

    user = User.objects.get(refresh_token=refresh_token)

    if user is None:
        raise User.DoesNotExist

    return user.access_token


def _authenticate_credentials(request, access_token):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        access_token = expired_token(request)

        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
    except jwt.DecodeError:
        msg = 'Authentication error. Invalid token.'
        raise exceptions.AuthenticationFailed(msg)
    except User.DoesNotExist:
        msg = 'The user corresponding to the given token was not found.'
        raise exceptions.AuthenticationFailed(msg)

    try:
        user = User.objects.get(pk=payload['id'])
    except User.DoesNotExist:
        msg = 'The user corresponding to the given token was not found.'
        raise exceptions.AuthenticationFailed(msg)

    if not user.is_active:
        msg = 'This user has been disabled.'
        raise exceptions.AuthenticationFailed(msg)

    request.COOKIES['access_token'] = access_token

    return user, access_token


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix and token is None:
            return None

        return _authenticate_credentials(request, token)
