# app/utils/cache.py — Cache simple en mémoire
import time
from functools import wraps

_cache = {}
_cache_time = {}


def cache_get(key):
    """Récupère une valeur du cache si pas expirée"""
    if key in _cache:
        if time.time() - _cache_time.get(key, 0) < 300:  # 5 minutes
            return _cache[key]
        del _cache[key]
        del _cache_time[key]
    return None


def cache_set(key, value):
    """Stocke une valeur dans le cache"""
    _cache[key] = value
    _cache_time[key] = time.time()


def cache_clear(key=None):
    """Vide le cache"""
    global _cache, _cache_time
    if key:
        _cache.pop(key, None)
        _cache_time.pop(key, None)
    else:
        _cache = {}
        _cache_time = {}


def cached(key_prefix, timeout=300):
    """Décorateur de cache pour les routes"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            cache_key = f"{key_prefix}_{str(args)}_{str(kwargs)}"
            result = cache_get(cache_key)
            if result is not None:
                return result
            result = f(*args, **kwargs)
            cache_set(cache_key, result)
            return result
        return wrapped
    return decorator
