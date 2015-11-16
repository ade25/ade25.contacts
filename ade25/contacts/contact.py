# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from Acquisition import aq_inner
from plone.app.content.interfaces import INameFromTitle
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer
from zope.interface import implements
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

    @property
    def title(self):
        if hasattr(self, 'first_name') and hasattr(self, 'last_name'):
            return '{0} {1}'.format(self.first_name, self.last_name)
        else:
            return ''

    def setTitle(self, value):
        return


class ITitleFromContactName(INameFromTitle):

    def title():
        """Return a processed title"""


class TitleFromContactName(object):
    implements(ITitleFromContactName)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return '{0} {1}'.format(self.context.first_name, self.context.last_name)

    def setTitle(self, value):
        return
