from django.db.models import Q


def filter_queryset(queryset, search, ordering, published_by, category):
    """ Filters the queryset with respect to the specified parameters, gives priority to search parameter. """

    if search:
        q_published_by = Q(published_by__username=search)
        q_category_name = Q(categories__name=search)
        queryset = queryset.filter(q_published_by | q_category_name)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    if published_by:
        queryset = queryset.filter(published_by__username=published_by)
    if category:
        queryset = queryset.filter(categories__name=category)
    if ordering:
        queryset = queryset.order_by(ordering)
    return queryset
