#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class CustomField(object):
    def __init__(self, json, requester):
        self.__requester = requester

        _message = json.get('message', None)
        if _message is not None:
            raise Exception("Error initiating %s class: %s" % (self.__name__, _message))

        self.customFieldId = json.get('customFieldId', None)
        self.enabled = json.get('enabled', None)
        self.name = json.get('name', None)
        self.organizationId = json.get('organizationId', None)
        self.value = json.get('value', None)
        self.type = json.get('type', None)
        if self.type is not None:
            self.type = CustomFieldType.createFromString(self.type)

        self._types = CustomFieldType()
        self._json = json

    def __eq__(self, other):
        return self.customFieldId == other.customFieldId

    def __hash__(self):
        return hash(self.customFieldId)


class CustomFieldType(object):
    NUMBER = u'Number'
    TEXT = u'Text'
    COLOR = u'Color'
    TIME = u'Time'

    @classmethod
    def createFromString(cls, data):
        colors = [cls.NUMBER, cls.TEXT, cls.COLOR, cls.TIME]

        if data in colors:
            return data

        raise Exception("wrong type %s" % data)
