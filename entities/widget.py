#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester
from .column import Column


class Widget(object):
    def __init__(self, json, requester):
        self._json = json
        self._requester = requester  # type: Requester

        self.archived = json.get('archived')
        self.collectionIds = json.get('collectionIds', [])
        self.color = json['color']  # type: str
        self.breakdownCardCommonId = json.get('breakdownCardCommonId', None)  # type: str
        self.editRole = json['editRole']  # type: str
        self.name = json['name']  # type: str
        self.organizationId = json.get('organizationId')
        self.ownerRole = json['ownerRole']  # type: str
        self.type = json['type']  # type: WidgetType
        self.widgetCommonId = json['widgetCommonId']  # type: str

    def __eq__(self, other):
        if not isinstance(other, Widget):
            return False
        return self.widgetCommonId == other.widgetCommonId

    def __hash__(self):
        return hash(self.widgetCommonId)

    def getColumns(self):
        """

        :rtype: list of Column
        """
        columnsJson = self._requester.getColumns(self.widgetCommonId)
        columns = []
        for columnJson in columnsJson['entities']:
            columns.append(Column(columnJson, self._requester))
        return columns

    def getCards(self, unique=False, todoListOnly=False):
        """

        :rtype: list of Card
        """
        from .card import Card
        filters = {'widgetCommonId': self.widgetCommonId}
        cardsJson = self._requester.getCards(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self._requester))
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
