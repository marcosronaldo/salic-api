from ...app import app


def build_brand_link(document):
    doc_id = document['id_arquivo']
    link_file = app.config['SALIC_BASE_URL'] + \
                'verprojetos/abrir?id=%d' % (doc_id)
    return link_file


def build_file_link(document):
    doc_id = document['idDocumentosAgentes']

    if document['Anexado'] == '2':
        idPronac = document['idPronac']
        link_file = app.config['SALIC_BASE_URL'] + \
                    'verprojetos/abrir-documentos-anexados?id=%d&tipo=2&idPronac=%d' % (
                        doc_id, idPronac)

    elif document['Anexado'] == '5':
        link_file = app.config['SALIC_BASE_URL'] + \
                    'verprojetos/abrir?id=%d' % (doc_id)

    else:
        link_file = ''

    return link_file
