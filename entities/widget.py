#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class Widget(object):
    def __init__(self, json):
        self.type = json['type']
        self.name = json['name']
        self.color = json['color']
        self.widgetCommonId = json['widgetCommonId']

    def __eq__(self, other):
        return self.widgetCommonId == other.widgetCommonId

    def __hash__(self):
        return hash(self.widgetCommonId)
