#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class Organization(object):
    def __init__(self, json, requester):
        self__requester = requester

        _message = json.get('message', None)
        if _message is not None:
            raise Exception("Error initiating Organization class: %s" % _message)

        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)

        self._json = json

    def __eq__(self, other):
        return self.organizationId == other.organizationId

    def __hash__(self):
        return hash(self.organizationId)
