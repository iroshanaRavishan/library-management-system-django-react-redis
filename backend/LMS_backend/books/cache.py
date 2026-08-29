from django.core.cache import cache


def invalidate_book_search_cache():
    """
    Remove all cached book-search results.
    """

    # Get all Redis keys used for book searches.
    keys = cache.keys("book_search:*")