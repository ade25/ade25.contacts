# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from Acquisition import aq_inner
from plone.app.content.interfaces import INameFromTitle
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer
from zope import schema

from ade25.sitecontent import MessageFactory as _


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


@implementer(IContentPage)
class Contact(Container):
    """ Content class """

    @property
    def title(self):
        first_name = getattr(self, 'first_name', None)
        last_name = getattr(self, 'last_name', None)
        if first_name and last_name:
            return '{0} {1}'.format(first_name, last_name)
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
        context = aq_inner(self.context)
        return '{0} {1}'.format(context.first_name, context.last_name)
