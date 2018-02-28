#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.widget import Widget


class WidgetService(object):
    def __init__(self, requester):
        super(WidgetService, self).__init__()
        self.requester = requester

    def getWidgets(self, collectionId):
        widgetsJson = self.requester.getWidgets(collectionId)
        widgets = []
        for widgetJson in widgetsJson['entities']:
            widgets.append(Widget(widgetJson))
        return widgets

    def getWidget(self, widgetCommonId):
        widgetJson = self.requester.getWidget(widgetCommonId)
        collection = Widget(widgetJson)
        return collection

    def getWidgetNames(self, widgets):
        return [widget.name for widget in widgets]

    def getWidgetByName(self, name, widgets):
        self.checkWidgetExists(name, widgets)
        return [widget for widget in widgets if widget.name == name][0]

    def checkWidgetExists(self, name, widgets):
        widgets_names = self.getWidgetNames(widgets)

        if name not in widgets_names:
            raise Exception("There's no such widget as " + name)

