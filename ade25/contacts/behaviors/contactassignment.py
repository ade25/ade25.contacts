# -*- coding: utf-8 -*-
"""Module providing contact information"""

from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform import directives
from plone.supermodel import model
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from plone.app.vocabularies.catalog import CatalogSource

from ade25.contacts import _


@provider(IFormFieldProvider)
class IContactAssignment(model.Schema):
    """Behavior allowing contact card assignment """

    # Contact card assignment fieldset
    model.fieldset(
        'contacts',
        label=u"Contact Cards",
        fields=['relatedContacts']
    )
    directives.widget('relatedContacts', RelatedItemsFieldWidget)
    relatedContacts = RelationList(
        title=u"Related Contacts",
        default=[],
        value_type=RelationChoice(
            title=_(u"Related"),
            source=CatalogSource(
                portal_type=['ade25.contacts.contact'],
                review_state="published"
            )
        ),
        required=False,
    )


@implementer(IContactAssignment)
@adapter(IDexterityContent)
class ContactAssignment(object):

    def __init__(self, context):
        self.context = context
