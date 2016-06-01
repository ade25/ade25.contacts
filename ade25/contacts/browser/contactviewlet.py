# -*- coding: utf-8 -*-
"""Module holding contact viewlet"""

from Acquisition import aq_inner
from plone import api
from plone.app.layout.viewlets import common as base

from ade25.contacts.behaviors.contactassignment import IContactAssignment


class ContactViewlet(base.ViewletBase):
    """ Display contact card for assigned contact items """

    def has_contact_card_assignment(self):
        """ Check for contact card assignment availability

        @return: True if IContactAssignment supported by context

        """
        context = aq_inner(self.context)
        if IContactAssignment.providedBy(context):
            return True
        return False

    def has_contacts(self):
        context = aq_inner(self.context)
        try:
            related_contacts = context.relatedContacts
        except AttributeError:
            related_contacts = None
        if related_contacts is not None:
            return True
        return False

    def contact_assignments(self):
        context = aq_inner(self.context)
        return context.relatedContacts

    def contact_cards(self):
        cards = list()
        for contact in self.contact_assignments():
            obj = contact.to_object
            if obj and not obj.display_element:
                cards.append(obj)
        return cards

    def contact_elements(self):
        elements = list()
        for contact in self.contact_assignments():
            obj = contact.to_object
            if obj and obj.display_element:
                elements.append(obj)
        return elements

    def rendered_contact_card(self, uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@contact-card-view')()
        return template

    def rendered_contact_element(self, uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@contact-element-view')()
        return template

    def render(self):
        """ Render viewlet only on items with enabled behavior

        """
        if self.has_contact_card_assignment():
            return super(ContactViewlet, self).render()
        else:
            return ""
