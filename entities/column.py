#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester


class Column(object):
    def __init__(self, json, requester):
        self._requester = requester  # type: Requester
        self.columnId = json['columnId']
        self.organizationId = json['organizationId']
        self.widgetCommonId = json['widgetCommonId']
        self.name = json['name']
        self.position = json['position']

        self._json = json

    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return self.columnId == other.columnId

    def __hash__(self):
        return hash(self.columnId)

    def update(self, new_name=None, new_position=None):
        """

        :rtype: Column
        """
        columnJson = self._requester.updateColumn(self.columnId, new_name, new_position)
        column = Column(columnJson, self._requester)
        return column

    def getCards(self, unique=False, todoListOnly=False):
        """

        :rtype: list of Card
        """
        from .card import Card
        filters = {'columnId': self.columnId}
        cardsJson = self._requester.getCardsByFilters(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self._requester))
        return cards

    def reposition(self, position):
        """

        :type position: int
        """
        if position == self.position:
            return
        output = self._requester._put('columns/' + self.columnId, json={'position': position})
        self.position = position
