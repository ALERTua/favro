#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester


class Organization(object):
    def __init__(self, json, requester):
        self._json = json
        self._requester = requester  # type: Requester

        _message = json.get('message', None)
        if _message is not None:
            raise Exception("Error initiating %s class: %s" % (self.__class__.__name__, _message))

        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)

    def __eq__(self, other):
        if not isinstance(other, Organization):
            return False
        return self.organizationId == other.organizationId

    def __hash__(self):
        return hash(self.organizationId)
