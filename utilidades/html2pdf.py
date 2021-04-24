# -*- coding: utf-8 -*-
import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/


    # convert URIs to absolute system paths
    # if uri.startswith(mUrl):
    #     print uri
    #     path = os.path.join(mRoot, uri.replace(mUrl, ""))
    # elif uri.startswith(sUrl):
    #     path = os.path.join(sRoot, uri.replace(sUrl, ""))
    # else:
    #     return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    path = settings.BASE_DIR + uri
    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), result, link_callback=link_callback)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def save_to_pdf(ruta_completa,template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    file = open(ruta_completa,"w+b")
    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), file, link_callback=link_callback)
    file.close()

    if not pdf.err:
        return file
    return None