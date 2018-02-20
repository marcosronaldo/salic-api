# from htmllaundry import strip_markup
# from BeautifulSoup import BeautifulStoneSoup
import cgi


def validate_cpf(digits):
    """
    Method to validate a brazilian CPF number
    Based on Pedro Werneck source avaiable at
    www.PythonBrasil.com.br

    Tests:
    >>> print(validate_cpf('91289037736'))
    True
    >>> print(validate_cpf('91289037731'))
    False
    """
    cpf_invalidos = [11 * str(i) for i in range(10)]

    # Verifica se o CPF contem pontos e hifens
    if digits in cpf_invalidos:
        return False
    elif not digits.isdigit():
        digits = digits.replace(".", "").replace("-", "")
    elif len(digits) != 11:
        return False

    digits = [int(x) for x in digits]
    data = digits[:9]

    # Confirma dígito verificador
    while len(data) < 11:
        r = sum((len(data) + 1 - i) * d for i, d in enumerate(data)) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        digits.append(f)

    return bool(digits == data)


def truncate(word, truncate_size=200):
    if word is None:
        return ""
    return word[:truncate_size]


def remove_blanks(word):
    if word is None:
        return ""

    return word.split()[0]


def cgccpf_mask(cgccpf):
    if validate_cpf(cgccpf):
        cgccpf = '***' + cgccpf[3:9] + '**'

    return cgccpf


def remove_html_tags(word):
    if word is None:
        return ""
    return word  # FIXME
    return strip_markup(word)


def HTMLEntitiesToUnicode(word):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    if word is None:
        return ""
    return word  # FIXME
    word = str(BeautifulStoneSoup(
        word, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    return word


def unicodeToHTMLEntities(word):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    word = cgi.escape(word).encode('ascii', 'xmlcharrefreplace')
    return text
