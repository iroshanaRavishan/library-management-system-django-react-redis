from django.core.cache import cache


def invalidate_book_search_cache():
    """
    Remove all cached book-search results.
    """

    # Get all Redis keys used for book searches.
    keys = cache.keys("book_search:*")

    # Delete the cached search results.
    if keys:
        cache.delete_many(keys)


def invalidate_book_detail_cache(book_id):
    """
    Remove the cached details of a specific book.
    """