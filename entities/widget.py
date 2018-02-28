#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from .column import Column
from .card import Card


class Widget(object):
    def __init__(self, json, requester):
        self.__requester = requester
        self.type = json['type']
        self.name = json['name']
        self.color = json['color']
        self.widgetCommonId = json['widgetCommonId']

        self._json = json

    def __eq__(self, other):
        return self.widgetCommonId == other.widgetCommonId

    def __hash__(self):
        return hash(self.widgetCommonId)

    def getColumns(self):
        columnsJson = self.__requester.getColumns(self.widgetCommonId)
        columns = []
        for columnJson in columnsJson['entities']:
            columns.append(Column(columnJson, self.__requester))
        return columns

    def getCards(self, unique=False, todoListOnly=False):
        filters = {'widgetCommonId': self.widgetCommonId}
        cardsJson = self.__requester.getCardsByFilters(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self.__requester))
        return cards
