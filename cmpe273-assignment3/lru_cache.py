import collections
import functools

def lru_cache(maxsize=10):
    def decorating_function(user_function):
        cache = collections.OrderedDict()    # order: least recent to most recent

        @functools.wraps(user_function)
        def wrapper(*args, **kwds):
            key = args
            try:
                result = cache.pop(key)
                print(f"[cache-hit] {user_function.__name__}({args[0]}) -> {result}")
                wrapper.hits += 1
            except KeyError:
                result = user_function(*args, **kwds)

                print(f"{user_function.__name__}({args[0]}) -> {result}")
                wrapper.misses += 1
                if len(cache) >= maxsize:
                    cache.popitem(0)
            cache[key] = result
            return result
        wrapper.hits = wrapper.misses = 0
        return wrapper
    return decorating_function


