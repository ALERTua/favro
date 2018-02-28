#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class User(object):
    def __init__(self, json):
        self.userId = json.get('userId', None)
        self.role = json.get('organizationRole', None)
        self.name = json.get('name', None)
        self.email = json.get('email', None)

    def __eq__(self, other):
        return self.userId == other.userId

    def __hash__(self):
        return hash(self.userId)
