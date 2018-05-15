#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from .column import Column
from .card import Card


class Widget(object):
    def __init__(self, json, requester):
        self.__requester = requester
        self.type = json['type']  # type: WidgetType
        self.name = json['name']  # type: str
        self.color = json['color']  # type: str
        self.widgetCommonId = json['widgetCommonId']  # type: str

        self._json = json

    def __eq__(self, other):
        return self.widgetCommonId == other.widgetCommonId

    def __hash__(self):
        return hash(self.widgetCommonId)

    def getColumns(self):
        """

        :rtype: list of Column
        """
        columnsJson = self.__requester.getColumns(self.widgetCommonId)
        columns = []
        for columnJson in columnsJson['entities']:
            columns.append(Column(columnJson, self.__requester))
        return columns

    def getCards(self, unique=False, todoListOnly=False):
        """

        :rtype: list of Card
        """
        filters = {'widgetCommonId': self.widgetCommonId}
        cardsJson = self.__requester.getCardsByFilters(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self.__requester))
        return cards


class WidgetType(object):
    BACKLOG = 'backlog'
    BOARD = 'board'

    @classmethod
    def createFromString(cls, data):
        types = [cls.BACKLOG, cls.BOARD]

        if data.lower() in types:
            return data.lower()

        raise Exception("wrong type %s" % data)
