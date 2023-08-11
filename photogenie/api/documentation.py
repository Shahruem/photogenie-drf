from drf_yasg import openapi


def get_user_posts_query_parameters():
    """ Returns query parameters for API documentation of list method of User Posts. """

    query_parameters = [
        openapi.Parameter(
            name='search',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Searches the post based on username or category provided.',
            required=False,
        ),
        openapi.Parameter(
            name='published_by',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Filters the post based on username.',
            required=False,
        ),
        openapi.Parameter(
            name='category',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Filters the post based on category name.',
            required=False,
        ),
        openapi.Parameter(
            name='ordering',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Sorts posts in ascending order based on views or downloads as provided.',
            required=False,
        ),
    ]

    return query_parameters
