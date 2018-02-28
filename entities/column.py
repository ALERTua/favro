#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class Column(object):
    def __init__(self, json, requester):
        self.requester = requester
        self.columnId = json['columnId']
        self.organizationId = json['organizationId']
        self.widgetCommonId = json['widgetCommonId']
        self.name = json['name']
        self.position = json['position']

    def __eq__(self, other):
        return self.columnId == other.columnId

    def __hash__(self):
        return hash(self.columnId)

    def update(self, new_name=None, new_position=None):
        columnJson = self.requester.updateColumn(self.columnId, new_name, new_position)
        column = Column(columnJson, self.requester)
        return column
