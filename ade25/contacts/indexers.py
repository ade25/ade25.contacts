# -*- coding: utf-8 -*-
"""Module providing a custom indexing setup for contacts"""
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.textfield.value import IRichTextValue
from plone.indexer.decorator import indexer

from ade25.contacts.contact import IContact


def _unicode_save_string_concat(*args):
    """
    concats args with spaces between and returns utf-8 string, it does not
    matter if input was unicode or str
    """
    result = ''
    for value in args:
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'replace')
        result = ' '.join((result, value))
    return result


def SearchableText(obj):
    text = u""
    richtext = IRichText(obj, None)
    if richtext:
        textvalue = richtext.text
        if IRichTextValue.providedBy(textvalue):
            transforms = getToolByName(obj, 'portal_transforms')
            text = transforms.convertTo(
                'text/plain',
                safe_unicode(textvalue.output).encode('utf8'),
                mimetype=textvalue.mimeType,
            ).getData().strip()

    subject = u' '.join(
        [safe_unicode(s) for s in obj.Subject()]
    )

    return u" ".join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u"",
        safe_unicode(obj.description) or u"",
        safe_unicode(text),
        safe_unicode(subject),
    ))


@indexer(IContact)
def SearchableText_contact(obj):
    return _unicode_save_string_concat(SearchableText(obj))
