# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer

from ade25.sitecontent import MessageFactory as _


class IContact(form.Schema, IImageScaleTraversable):
    """
    A folderish page
    """


@implementer(IContentPage)
class Contact(Container):
    pass
