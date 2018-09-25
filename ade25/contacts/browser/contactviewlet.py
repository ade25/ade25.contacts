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

    @staticmethod
    def _contact_object_is_published(obj):
        contact_state = api.content.get_state(obj)
        if contact_state == 'published':
            return True
        return False

    def available_contact_assigments(self):
        assignments = self.contact_assignments()
        public_contacts = list()
        for contact in assignments:
            if not contact.isBroken():
                obj = contact.to_object
                if api.user.is_anonymous():
                    # Prevent errors caused by private target objects
                    if self._contact_object_is_published(obj):
                        public_contacts.append(obj)
                else:
                    public_contacts.append(obj)
        return public_contacts

    def contact_cards(self):
        cards = list()
        for contact in self.available_contact_assigments():
            if not contact.display_element:
                cards.append(contact)
        return cards

    def contact_elements(self):
        elements = list()
        for contact in self.available_contact_assigments():
            if contact.display_element:
                elements.append(contact)
        return elements

    def rendered_contact_card(self, uuid):
        context = aq_inner(self.context)
        obj = api.content.get(UID=uuid)
        template = obj.restrictedTraverse('@@contact-card-view')(
            uuid=context.UID()
        )
        return template

    def rendered_contact_element(self, uuid):
        context = aq_inner(self.context)
        obj = api.content.get(UID=uuid)
        try:
            template = obj.restrictedTraverse('@@contact-element-view')(
                uuid=context.UID()
            )
        except AttributeError:
            return
        return template

    def render(self):
        """ Render viewlet only on items with enabled behavior

        """
        if self.has_contact_card_assignment():
            return super(ContactViewlet, self).render()
        else:
            return ""
