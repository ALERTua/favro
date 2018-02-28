#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.tag import Tag, TagColor


class TagService(object):
    def __init__(self, requester):
        self.requester = requester

    def getTags(self, name=None):
        tagsJson = self.requester.getTags(name)
        tags = []
        for tagJson in tagsJson['entities']:
            tags.append(Tag(tagJson, self.requester))
        return tags

    def getTagByName(self, name):
        return self.getTags(name)

    def getTagById(self, tagId):
        return self.requester.getTag(tagId)

    def createTag(self, name, color=None):
        if color is not None:
            color = TagColor.createFromString(color)
        tagJson = self.requester.createTag(name, color)
        tag = Tag(tagJson, self.requester)
        return tag
