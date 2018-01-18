import datetime
import decimal
import json
import logging

import dicttoxml

log = logging.getLogger('dicttoxml')
log.setLevel(logging.ERROR)


def listify_queryset(queryset):
    """
    Returns a fully serializable list of dictionaries
    """
    return list(map(convert_object, queryset))


def serialize(data, format):
    """
    Return a string of serialized data for the given output format.
    """
    if format == 'xml':
        return to_xml(data)
    elif format == 'json':
        return to_json(data)
    elif format == 'csv':
        return to_csv(data)
    else:
        raise ValueError('invalid format: %s' % format)


def convert_atom(x):
    """
    Convert atomic Python data type to JSON compatible value.
    """
    if isinstance(x, decimal.Decimal):
        return float(x)
    elif isinstance(x, datetime.date):
        return str(x)
    return x


def convert_object(x):
    """
    Convert an instance of a queryset to a JSON compatible value.
    """
    return dict(zip(x.keys(), map(convert_atom, x)))


def to_xml(data):
    return dicttoxml.dicttoxml(data)


def to_json(data):
    return json.dumps(data, ensure_ascii=False)


def to_csv(data):
    if isinstance(data, dict):
        keys = list(data.keys())
        data = [data, ]

    else:
        keys = list(data[0].keys())

    csv_data = ""
    csv_data += keys[0]

    for key_index in range(1, len(keys)):
        csv_data += ',%s' % (keys[key_index])

    csv_data += "\n"
    for data_row in data:

        # First item, especial case
        item = data_row[keys[0]]

        if item is None:
            uni_data = ''

        elif isinstance(item, float) or isinstance(item, int):
            uni_data = str(item).decode('utf8')

        elif isinstance(item, list) or isinstance(item,
                                                  dict):  # TODO: fix these special cases
            uni_data = "null"
        else:
            uni_data = '\"' + item + '\"'

        csv_data += '%s' % (uni_data)

        # Remaining items
        for key_index in range(1, len(keys)):
            item = data_row[keys[key_index]]

            if item is None:
                uni_data = ''

            elif isinstance(item, float) or isinstance(item, int):
                uni_data = str(item).decode('utf8')

            # TODO: fix these special cases
            elif isinstance(item, list) or isinstance(item, dict):
                uni_data = "null"
            else:
                uni_data = '\"' + item + '\"'

            csv_data += ',%s' % (uni_data)

        csv_data += "\n"

    return csv_data
