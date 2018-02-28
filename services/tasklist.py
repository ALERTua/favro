#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.card import Card
from ..entities.task import Task
from ..entities.tasklist import TaskList


class TaskListService(object):
    def __init__(self, requester):
        self.requester = requester

    def getTaskLists(self, card_or_cardcommonId):
        cardId = card_or_cardcommonId
        if isinstance(card_or_cardcommonId, Card):
            cardId = card_or_cardcommonId.cardCommonId

        taskListsJson = self.requester.getTaskLists(cardId)
        taskLists = []
        for taskListJson in taskListsJson.get('entities', {}):
            tasklist = TaskList(taskListJson, self.requester)
            taskLists.append(tasklist)

        return list(set(taskLists))

    def getTaskList(self, taskListId):
        taskListJson = self.requester.getTaskList(taskListId)
        taskList = TaskList(taskListJson, self.requester)
        return taskList

    def createTaskList(self, card_or_Id, name, position=None, tasks=None):
        cardId = card_or_Id
        if isinstance(card_or_Id, Card):
            cardId = card_or_Id.cardId

        if tasks is not None:
            for task in tasks:
                if not isinstance(task, Task):
                    raise Exception("createTaskList: tasks must contain only Task objects")

        taskListJson = self.requester.createTaskList(cardId, name, position, tasks)
        taskList = TaskList(taskListJson, self.requester)
        return taskList
