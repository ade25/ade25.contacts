# -*- coding: utf-8 -*-
"""Module providing views for contact page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.component import getUtility

from ade25.contacts.interfaces import IContactImagesTool


class ContactView(BrowserView):
    """ Folderish contact item default view """

    def has_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def has_address_info(self):
        context = aq_inner(self.context)
        if context.address or context.city:
            return True
        return False

    def has_position_info(self):
        context = aq_inner(self.context)
        if context.position or context.department:
            return True
        return False

    def get_image_data(self, uuid):
        tool = getUtility(IContactImagesTool)
        return tool.create(uuid)

    def render_contact_card(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@contact-card-view')()
        return template


class ContactCardView(BrowserView):
    """ Card view for contact objects """

    def has_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def has_address_info(self):
        context = aq_inner(self.context)
        if context.address or context.city:
            return True
        return False

    def get_image_data(self, uuid):
        tool = getUtility(IContactImagesTool)
        return tool.create(uuid)
