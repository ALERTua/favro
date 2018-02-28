#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class Tag(object):
    # https://favro.com/developer/#tags
    def __init__(self, json, requester):
        self.__requester = requester
        self.tagId = json.get('tagId', None)
        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)
        self.color = TagColor.createFromString(json.get('color'))

        self._json = json

    def __eq__(self, other):
        return self.tagId == other.tagId

    def __hash__(self):
        return hash(self.tagId)

    def update(self, name=None, color=None):
        if color is not None:
            color = TagColor.createFromString(color)

        tagJson = self.__requester.updateTag(self.tagId, name, color)
        tag = Tag(tagJson, self.__requester)
        return tag

    def delete(self):
        return self.__requester.deleteTag(self.tagId)


class TagColor(object):
    # https://favro.com/developer/#tag-colors
    BLUE = 'blue'
    PURPLE = 'purple'
    CYAN = 'cyan'
    GREEN = 'green'
    LIGHTGREEN = 'lightgreen'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    RED = 'red'
    BROWN = 'brown'
    GRAY = 'gray'
    SLATEGRAY = 'slategray'

    @classmethod
    def createFromString(cls, data):
        colors = [cls.BLUE, cls.PURPLE, cls.CYAN, cls.GREEN, cls.LIGHTGREEN, cls.YELLOW, cls.ORANGE, cls.RED,
                  cls.BROWN, cls.GRAY, cls.SLATEGRAY]

        if data.lower() in colors:
            return data.lower()

        raise Exception("wrong color %s" % data)
