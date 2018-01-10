import datetime
import decimal
import json
import logging

import dicttoxml

log = logging.getLogger('dicttoxml')
log.setLevel(logging.ERROR)


def to_xml(data):
    return dicttoxml.dicttoxml(data)


def to_json(data):
    return json.dumps(data, ensure_ascii=False, encoding='utf-8')


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


def list_serializable(l):
    l_serializable = []

    for e in l:
        if isinstance(e, decimal.Decimal):
            l_serializable.append(float(e))
        elif isinstance(e, datetime.date):
            l_serializable.append(str(e))
        else:
            l_serializable.append(e)

    return l_serializable


def listsTodict(keys, values):
    values_list = []

    for value in values:
        values_list.append(value)

    return dict(list(zip(keys, list_serializable(values_list))))


def listify_queryset(queryset):
    # Returns a fully serializable list of dictionaries

    result = []

    for d in queryset:
        result.append(listsTodict(list(d.keys()), d))

    return result


def serialize(data, out_format):
    if out_format == 'xml':
        return to_xml(data)

    elif out_format == 'json':
        return to_json(data)

    elif out_format == 'csv':
        return to_csv(data)


def to_hal(resource, resource_links):
    resource["_links"] = resource_links
