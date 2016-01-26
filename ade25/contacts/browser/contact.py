# -*- coding: utf-8 -*-
"""Module providing views for contact page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.component import getUtility

from ade25.contacts.interfaces import IResponsiveImagesTool


class ContactView(BrowserView):
    """ Folderish contact item default view """


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
        tool = getUtility(IResponsiveImagesTool)
        return tool.create(uuid)
