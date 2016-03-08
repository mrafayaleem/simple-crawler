import hashlib


def url_hash(url):
    """Function to calculate hash of url."""

    return hashlib.md5(url).hexdigest()
