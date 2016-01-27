# -*- coding: utf-8 -*-
"""Module holding contact viewlet"""

from Acquisition import aq_inner
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

    def render(self):
        """ Render viewlet only on items with enabled behavior

        """
        if self.has_contact_card_assignment():
            return super(ContactViewlet, self).render()
        else:
            return ""
