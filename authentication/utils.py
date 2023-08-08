from rest_framework_simplejwt.tokens import RefreshToken


def get_user_tokens(user):
    """ Returns the access and refresh token of passed-in user in form of a dictionary """

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
