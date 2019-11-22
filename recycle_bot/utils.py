import difflib
import json

from functools import wraps


def to_tg_update(bot):
    from telegram import Update

    def wrapped(fn):
        @wraps(fn)
        def inner(event, *args, **kwargs):
            update = Update.de_json(json.loads(event.get('body')), bot)
            return fn(update, *args, **kwargs)
        return inner
    return wrapped


def predict_key(key, keys, words=1):
    return difflib.get_close_matches(key, keys, words, 0)
