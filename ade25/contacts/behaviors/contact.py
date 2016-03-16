# -*- coding: utf-8 -*-
"""Module providing contact information"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope import schema

from ade25.contacts import _


@provider(IFormFieldProvider)
class IContactInformation(model.Schema):
    """Behavior providing contact information"""

    position = schema.TextLine(
        title=_(u"Position"),
        required=False
    )

    department = schema.TextLine(
        title=_(u"Department"),
        required=False
    )

    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False
    )

    fax = schema.TextLine(
        title=_(u"Fax"),
        required=False
    )

    url = schema.TextLine(
        title=_(u"URL"),
        required=False
    )

    email = schema.TextLine(
        title=_(u"E-Mail"),
        required=False
    )

    enquiry = schema.Bool(
        title=_(u"Check to enable direct enquiry"),
        description=_(u"When activated the contact card will link to an "
                      u"direct enquiry form"),
        required=False,
    )

    # Contact address details fieldset
    model.fieldset(
        'details',
        label=u"Contact Details",
        fields=['city', 'zipcode', 'address', 'address_extra']
    )
    city = schema.TextLine(
        title=_(u"City"),
        required=False
    )
    zipcode = schema.TextLine(
        title=_(u"Zipcode"),
        required=False
    )
    address = schema.TextLine(
        title=_(u"Address"),
        required=False
    )
    address_extra = schema.TextLine(
        title=_(u"Address Additional"),
        required=False
    )

    model.fieldset(
        'display',
        label=u"Contact Display",
        fields=['display_element']
    )
    display_element = schema.Bool(
        title=_(u"Check to enable content element display"),
        description=_(u"When activated the view will attempt to display a "
                      u"content element instead of a contact card"),
        required=False,
    )


@implementer(IContactInformation)
@adapter(IDexterityContent)
class ContactInformation(object):

    def __init__(self, context):
        self.context = context
