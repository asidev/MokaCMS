#!/usr/bin/env python
import colander
from .types import URI
__all__ = ['MenuSchema']


class MenuItem(colander.MappingSchema):
    label = colander.SchemaNode(colander.String())
    url = colander.SchemaNode(URI(), default=None, missing=None)
    #children = MenuItems()


class MenuItems(colander.SequenceSchema):
    item = MenuItem()


# Avoid circular dep.
MenuItem.children = MenuItems()


class MenuTranslation(colander.MappingSchema):
    language = colander.SchemaNode(colander.String())
    items = MenuItems()


class MenuTranslations(colander.SequenceSchema):
    translation = MenuTranslation()


class MenuSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    translations = MenuTranslations()


class MenusCollectionSchema(colander.SequenceSchema):
    menu = MenuSchema()
