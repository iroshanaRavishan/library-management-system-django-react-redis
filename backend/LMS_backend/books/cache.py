from django.core.cache import cache


def invalidate_book_search_cache():
    """
    Remove all cached book-search results.
    """