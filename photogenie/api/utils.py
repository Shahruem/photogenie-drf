from django.db.models import Q


def filter_user_posts(queryset, query_parameters):
    """ Filters the queryset with respect to the specified query parameters, gives priority to search parameter. """

    search = query_parameters.get('search', None)
    published_by = query_parameters.get('published_by', None)
    category = query_parameters.get('category', None)
    ordering = query_parameters.get('ordering', None)
    print(search)

    if search:
        q_published_by = Q(published_by__username=search)
        q_category_name = Q(categories__name=search)
        queryset = queryset.filter(q_published_by | q_category_name)
        return queryset

    if published_by:
        queryset = queryset.filter(published_by__username=published_by)
    if category:
        queryset = queryset.filter(categories__name=category)
    if ordering:
        queryset = queryset.order_by(ordering)
    return queryset
