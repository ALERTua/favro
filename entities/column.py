#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester


class Column(object):
    def __init__(self, json, requester):
        self._json = json
        self._requester = requester  # type: Requester

        self.cardCount = json['cardCount']  # type: int
        self.columnId = json['columnId']  # type: str
        self.estimationSum = json.get('estimationSum', None)  # type: int
        self.name = json['name']  # type: str
        self.organizationId = json['organizationId']  # type: str
        self.position = json['position']  # type: float
        self.timeSum = json.get('timeSum', None)  # type: int
        self.widgetCommonId = json['widgetCommonId']  # type: str

    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return self.columnId == other.columnId

    def __hash__(self):
        return hash(self.columnId)

    def __str__(self):
        return self.name

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
        cardsJson = self._requester.getCards(filters, unique, todoListOnly)
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
