#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.column import Column
from ..entities.widget import Widget


class ColumnService(object):
    def __init__(self, requester):
        self.__requester = requester

    def getColumn(self, columnId):
        columnJson = self.__requester.getColumn(columnId)
        column = Column(columnJson, self.__requester)
        return column

    def getColumnByName(self, name, columns):
        for column in columns:
            if column.name == name:
                return column
        return None

    def createColumn(self, widget_or_widgetCommonId, column_name, position=None):
        widgetCommonId = widget_or_widgetCommonId
        if isinstance(widget_or_widgetCommonId, Widget):
            widgetCommonId = widget_or_widgetCommonId.widgetCommonId

        columnJson = self.__requester.createColumn(widgetCommonId, column_name, position)
        column = Column(columnJson, self.__requester)
        return column
