#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.column import Column


class ColumnService(object):
    def __init__(self, requester):
        self.requester = requester

    def getColumns(self, widget_or_widgetCommonId):
        from ..entities.widget import Widget
        widgetCommonId = widget_or_widgetCommonId
        if isinstance(widget_or_widgetCommonId, Widget):
            widgetCommonId = widget_or_widgetCommonId.widgetCommonId

        columnsJson = self.requester.getColumns(widgetCommonId)
        columns = []
        for columnJson in columnsJson['entities']:
            columns.append(Column(columnJson, self.requester))
        return columns

    def getColumn(self, columnId):
        columnJson = self.requester.getColumn(columnId)
        column = Column(columnJson, self.requester)
        return column

    def getColumnByName(self, name, columns):
        for column in columns:
            if column.name == name:
                return column
        return None

    def createColumn(self, name, position=0):
        # todo
        pass
