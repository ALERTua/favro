#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class Collection(object):
    def __init__(self, json):
        from .user import User
        self.name = json['name']
        self.collectionId = json['collectionId']
        self.publicSharing = json['publicSharing']
        self.archived = json['archived']
        self.users = []
        for jsonUser in json['sharedToUsers']:
            self.users.append(User(jsonUser))

    def __eq__(self, other):
        return self.collectionId == other.collectionId

    def __hash__(self):
        return hash(self.collectionId)
