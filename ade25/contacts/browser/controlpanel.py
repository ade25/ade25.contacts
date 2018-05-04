# -*- coding: utf-8 -*-
"""Module providing contacts control panel"""
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.z3cform import layout
from zope import schema
from zope.interface import Interface

from ade25.contacts import _


class IAde25ContactsControlPanel(Interface):
    """ Contacts settings """

    display_privacy_policy = schema.Bool(
        title=_(u"Enable Privacy Policy fields"),
        description=_(u"Select if a privacy notice and policy agreement "
                      u"checkbox should be added to inquiry forms."),
        default=False,
        required=False
    )

    privacy_policy_url = schema.TextLine(
        title=_(u"Privacy Policy Location"),
        description=_(u"Enter relative location of privacy and data "
                      u"protection notice page"),
        default=u'/datenschutzerklaerung',
        required=False
    )


class Ade25ContactsControlPanelForm(RegistryEditForm):
    schema = IAde25ContactsControlPanel
    schema_prefix = "ade25.contacts"
    label = u'Ade25 Contacts Settings'


Ade25ContactsSettings = layout.wrap_form(
    Ade25ContactsControlPanelForm,
    ControlPanelFormWrapper
)