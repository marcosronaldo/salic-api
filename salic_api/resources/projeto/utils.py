from flask import current_app

#FIXME descobrir como faremos para retornar esses links do salic.
def build_brand_link(document):
    doc_id = document['id_arquivo']
    base_url = current_app.config.get('SALIC_BASE_URL')
    if base_url is None: return ''
    link_file = base_url + \
        'verprojetos/abrir?id=%d' % (doc_id)
    return link_file


def build_file_link(document):
    doc_id = document['idDocumentosAgentes']

    if document['Anexado'] == '2':
        idPronac = document['idPronac']
        link_file = current_app.config['SALIC_BASE_URL'] + \
            'verprojetos/abrir-documentos-anexados?id=%d&tipo=2&idPronac=%d' % (
            doc_id, idPronac)

    elif document['Anexado'] == '5':
        link_file = current_app.config['SALIC_BASE_URL'] + \
            'verprojetos/abrir?id=%d' % (doc_id)

    else:
        link_file = ''

    return link_file
