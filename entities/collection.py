#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester
from .widget import Widget, WidgetType
from .user import User


class Collection(object):
    def __init__(self, json, requester):
        self._json = json
        self._requester = requester  # type: Requester

        self.archived = json['archived']
        self.background = json.get('background', None)
        self.collectionId = json['collectionId']
        self.fullMembersCanAddWidgets = json.get('fullMembersCanAddWidgets', None)
        self.name = json['name']
        self.organizationId = json['organizationId']
        self.publicSharing = json.get('publicSharing', None)

        self.sharedToUsers = []
        for jsonUser in json['sharedToUsers']:
            self.sharedToUsers.append(User(jsonUser, self._requester))

    def __eq__(self, other):
        if not isinstance(other, Collection):
            return False
        return self.collectionId == other.collectionId

    def __hash__(self):
        return hash(self.collectionId)

    def __str__(self):
        return self.name

    def getWidgets(self):
        """

        :rtype: list of Widget
        """
        widgetsJson = self._requester.getWidgets(self.collectionId)
        widgets = []
        for widgetJson in widgetsJson['entities']:
            widgets.append(Widget(widgetJson, self._requester))
        return widgets

    def getCards(self, unique=False, todoListOnly=False):
        """

        :rtype: list of Card
        """
        from .card import Card
        filters = {'collectionId': self.collectionId}
        cardsJson = self._requester.getCards(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self._requester))
        return cards

    def createWidget(self, widgetName, widgetType):
        """

        :rtype: Widget
        :type widgetType: WidgetType
        :type widgetName: str
        """
        return Widget(self._requester.createWidget(widgetName, widgetType, self.collectionId), self._requester)
