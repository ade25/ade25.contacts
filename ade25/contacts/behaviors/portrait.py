# -*- coding: utf-8 -*-
from plone.app.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IPortrait(model.Schema):

    image = namedfile.NamedBlobImage(
        title=_(u'Portrait'),
        description=_(u'Add portrait image for contact card'),
        required=False,
    )


@implementer(IPortrait)
@adapter(IDexterityContent)
class Portrait(object):

    def __init__(self, context):
        self.context = context
