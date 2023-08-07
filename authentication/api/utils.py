
def validate_data(serializer_class, data):
    """ Validates data according to provided serializer class. """

    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
