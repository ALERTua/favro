#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.widget import Widget


class WidgetService(object):
    def __init__(self, requester):
        super(WidgetService, self).__init__()
        self.__requester = requester

    def getWidget(self, widgetCommonId):
        """

        :rtype: Widget
        """
        widgetJson = self.__requester.getWidget(widgetCommonId)
        widget = Widget(widgetJson, self.__requester)
        return widget

    def getWidgetNames(self, widgetsList):
        return [widget.name for widget in widgetsList]

    def getWidgetByName(self, name, widgetsList):
        """

        :rtype: Widget
        """
        self.checkWidgetExists(name, widgetsList)
        return [widget for widget in widgetsList if widget.name == name][0]

    def checkWidgetExists(self, name, widgetsList):
        """

        :rtype: bool
        """
        widgets_names = self.getWidgetNames(widgetsList)
        return name in widgets_names

