from django.core.cache import cache

from dashboard.cache_keys import DASHBOARD_CACHE_KEY


def invalidate_dashboard_cache():
    """
    Invalidate cached dashboard statistics.

    The next dashboard request will calculate
    fresh statistics and cache them again.
    """
    cache.delete(DASHBOARD_CACHE_KEY)