#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester
from .widget import Widget, WidgetType
from .user import User


class Collection(object):
    def __init__(self, json, requester):
        self.__requester = requester  # type: Requester
        self.name = json['name']
        self.collectionId = json['collectionId']
        self.publicSharing = json['publicSharing']
        self.archived = json['archived']
        self.users = []
        for jsonUser in json['sharedToUsers']:
            self.users.append(User(jsonUser, self.__requester))

        self._json = json

    def __eq__(self, other):
        return self.collectionId == other.collectionId

    def __hash__(self):
        return hash(self.collectionId)

    def getWidgets(self):
        """

        :rtype: list of Widget
        """
        widgetsJson = self.__requester.getWidgets(self.collectionId)
        widgets = []
        for widgetJson in widgetsJson['entities']:
            widgets.append(Widget(widgetJson, self.__requester))
        return widgets

    def getCards(self, unique=False, todoListOnly=False):
        """

        :rtype: list of Card
        """
        from .card import Card
        filters = {'collectionId': self.collectionId}
        cardsJson = self.__requester.getCardsByFilters(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self.__requester))
        return cards

    def createWidget(self, widgetName, widgetType):
        """

        :rtype: Widget
        :type widgetType: WidgetType
        :type widgetName: str
        """
        return Widget(self.__requester.createWidget(widgetName, widgetType, self.collectionId), self.__requester)
