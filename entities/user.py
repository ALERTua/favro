#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester


class User(object):
    def __init__(self, json, requester):
        self._json = json
        self._requester = requester  # type: Requester

        self.userId = json.get('userId', None)
        self.organizationRole = json.get('organizationRole', None)
        self.name = json.get('name', None)
        self.email = json.get('email', None)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.userId == other.userId

    def __hash__(self):
        return hash(self.userId)
