from urlparse import urlparse


def is_url_in_domain(url, domains):
    parsed = urlparse(url)
    for domain in domains:
        if domain.match(parsed.netloc):
            return True

    return False


def is_absolute(url):
    return bool(urlparse(url).netloc)
