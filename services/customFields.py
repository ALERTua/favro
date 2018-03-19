#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.customField import CustomField


class CustomFieldService(object):
    def __init__(self, requester):
        self.__requester = requester

    def getCustomFields(self):
        """

        :rtype: list of CustomField
        """
        customFieldsJson = self.__requester.getCustomFields()
        customFields = []
        for customFieldJson in customFieldsJson['entities']:
            customFields.append(CustomField(customFieldJson, self.__requester))
        return customFields

    def getCustomField(self, customFieldId):
        """

        :rtype: CustomField
        """
        customFieldsJson = self.__requester.getCustomField(customFieldId)
        customField = CustomField(customFieldsJson, self.__requester)
        return customField

    def getCustomFieldByFilter(self, name, _type):
        """

        :rtype: CustomField
        """
        customFields = self.getCustomFields()
        for customField in customFields:
            if customField.name == name:
                if customField.type == _type:
                    return customField
        raise Exception("There's no such customField as %s:%s" % (name, _type))
