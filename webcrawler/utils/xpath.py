
RELATIVE_URL_TEMPLATE = "(//@href)[{not_extension_clause} and (.)[not(starts-with(.,'//'))][not(starts-with(.,'https://'))][not(starts-with(.,'http://'))]]"

ABS_URL_TEMPLATE = "(//@href)[{not_extension_clause} and (starts-with(.,'//') or starts-with(.,'https://') or starts-with(.,'http://'))]"


def build_relative_url_xpath(ignored_extensions):
    """Builds xpath expression containing extension regexes."""

    exts = '|'.join(ignored_extensions)
    not_extension_clause = "not(re:test(., '({exts})$'))".format(exts=exts)

    final_path = RELATIVE_URL_TEMPLATE.format(
        not_extension_clause=not_extension_clause
    )

    return final_path


def build_abs_url_xpath(ignored_extensions):
    """Builds xpath expression containing extension regexes."""

    exts = '|'.join(ignored_extensions)
    not_extension_clause = "not(re:test(., '({exts})$'))".format(exts=exts)

    final_path = ABS_URL_TEMPLATE.format(
        not_extension_clause=not_extension_clause
    )

    return final_path
