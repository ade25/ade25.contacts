# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ade25.contact.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ade25.contact into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ade25.contact is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ade25.contact'))

    def test_uninstall(self):
        """Test if ade25.contact is cleanly uninstalled."""
        self.installer.uninstallProducts(['ade25.contact'])
        self.assertFalse(self.installer.isProductInstalled('ade25.contact'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IAde25ContactLayer is registered."""
        from ade25.contact.interfaces import IAde25ContactLayer
        from plone.browserlayer import utils
        self.failUnless(IAde25ContactLayer in utils.registered_layers())
