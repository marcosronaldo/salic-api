import re

from .format_utils import truncate, remove_html_tags, HTMLEntitiesToUnicode


def sanitize(value, truncated=True, keep_markup=False):
    if value is None:
        return ""

    if not keep_markup:
        value = remove_html_tags(value)
        value = HTMLEntitiesToUnicode(value)

    if truncated:
        value = truncate(value)

    value = value.replace('"', '')

    # Removing tabs, newlines and other "whitespace-like" characters.
    value = re.sub('\s+', ' ', value).strip()

    return value
