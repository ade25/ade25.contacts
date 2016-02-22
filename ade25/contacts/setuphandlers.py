# -*- coding: utf-8 -*-
"""Module providing custom setup handlers"""
import logging
from plone import api

PROFILE_ID = 'profile-ade25.contacts:default'


def setupCatalogIndexes(context, logger=None):
    """ Method to add our wanted indexes to the portal_catalog """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('ade25.contacts')

    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = api.portal.get_tool(name='portal_catalog')
    indexes = catalog.indexes()

    # Specify the indexes you want
    # Format is: ('index_name', 'index_type')
    wanted = (
        ('display_element', 'BooleanIndex'),
    )

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('ade25.contacts-various.txt') is None:
        return
    portal = api.portal.get()

    setupCatalogIndexes(portal)
