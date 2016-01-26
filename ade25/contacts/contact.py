# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer
from zope import schema

from ade25.contacts import _


class IContact(form.Schema, IImageScaleTraversable):
    """
    A folderish page
    """

    first_name = schema.TextLine(
        title=_(u"First name"),
        required=True
    )

    last_name = schema.TextLine(
        title=_(u"Last name"),
        required=True
    )


@implementer(IContact)
class Contact(Container):
    """ Content class """
