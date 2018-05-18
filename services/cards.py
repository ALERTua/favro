#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester
from ..entities.card import Card


class CardService(object):
    def __init__(self, requester):
        self._requester = requester  # type: Requester

    def _getCardsByFilter(self, filters, unique=False, todoListOnly=False):
        """

        :rtype: list of Card
        """
        cardsJson = self._requester.getCardsByFilters(filters, unique, todoListOnly)
        cards = []
        for cardJson in cardsJson['entities']:
            cards.append(Card(cardJson, self._requester))
        return cards

    def getCardsByCardCommonId(self, cardCommonId, unique=False, todoListOnly=False):
        filters = {'cardCommonId': cardCommonId}
        return self._getCardsByFilter(filters, unique, todoListOnly)

    def getCardsByCardSequentialId(self, cardSequentialId, unique=False, todoListOnly=False):
        filters = {'cardSequentialId': cardSequentialId}
        return self._getCardsByFilter(filters, unique, todoListOnly)

    def getCard(self, card_or_Id):
        """
        :rtype: Card
        """
        cardId = card_or_Id
        if isinstance(card_or_Id, Card):
            cardId = card_or_Id.cardId
        cardJson = self._requester.getCard(cardId)
        card = Card(cardJson, self._requester)
        return card

    def createCard(self, name, widgetCommonId=None, laneId=None, columnId=None, parentCard_or_CardId=None,
                   detailedDescription=None, position=None, assignmentIds=None, tagsNamesList=None, tagIdsList=None,
                   startDate=None, dueDate=None, tasklistsList=None, customFields=None):
        """
        https://favro.com/developer/#create-a-card

        :param name: The name of the card. Required.
        :type name: str

        :param widgetCommonId: The widgetCommonId to create the card on. If not set, the card will be created in the user’s to do list.
        :type widgetCommonId: str

        :param laneId: The laneId to create the card in. This is only applicable if creating the card on a widget that has lanes enabled. Optional.
        :type laneId: str

        :param columnId: The columnId to create the card in. It must belong to the widget specified in the widgetCommonId parameter. WidgetCommonId is required if this parameter is set.
        :type columnId: str

        :param parentCard_or_CardId: If creating a card on a backlog widget, it is possible to create this card as a child of the card specified by this parameter. Optional.

        :param detailedDescription: The detailed description of the card. Supports formatting.
        :type detailedDescription: str

        :param position: Position of the card in the list.
        :type position: int

        :param assignmentIds: The list of assignments (array of userIds). Optional.
        :type assignmentIds: list

        :param tagsNamesList: The list of tag names or card tags that will be added to card. If current tag is not exist in the organization, it will be created.
        :type tagsNamesList: list

        :param tagIdsList: The list of tag IDs, that will be added to card.
        :type tagIdsList: list

        :param startDate: The start date of card. Format ISO-8601.
        :type startDate: str

        :param dueDate: The due date of card. Format ISO-8601.
        :type dueDate: str

        :param tasklistsList: The list of card tasklists.
        :type tasklistsList: list

        :param customFields: The list of card custom field parameters.
        :type customFields: dict

        :return:
        :rtype: Card
        """
        json = {'name': name}

        if widgetCommonId is not None:
            json['widgetCommonId'] = widgetCommonId

        if laneId is not None:
            json['laneId'] = laneId

        if columnId is not None:
            if not widgetCommonId:
                raise Exception("createCard: columnId can be specified only with widgetCommonId")
            json['columnId'] = columnId

        if parentCard_or_CardId is not None:
            parentCardId = parentCard_or_CardId
            if isinstance(parentCard_or_CardId, Card):
                parentCardId = parentCard_or_CardId.cardId

            json['parentCardId'] = parentCardId

        if detailedDescription is not None:
            # *italic*, **bold**, ```code block```, [Link](“http://localhost”)
            json['detailedDescription'] = detailedDescription

        if position is not None:
            json['position'] = position

        if assignmentIds is not None:
            json['assignmentIds'] = assignmentIds

        if tagsNamesList is not None:
            json['tags'] = tagsNamesList

        if tagIdsList is not None:
            json['tagIds'] = tagIdsList

        if startDate is not None:
            # todo: Format ISO-8601
            json['startDate'] = startDate

        if dueDate is not None:
            # todo: Format ISO-8601
            json['dueDate'] = dueDate

        if tasklistsList is not None:
            json['tasklists'] = tasklistsList
            # for task in tasklistsList:
            #    if not isinstance(task, TaskList):
            #        raise Exception("createCard: tasklistsList must contain only TaskList objects")

        if customFields is not None:
            json['customFields'] = customFields

        cardJson = self._requester.createCard(**json)
        card = Card(cardJson, self._requester)
        return card
