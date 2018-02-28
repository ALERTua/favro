#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.card import Card
from ..entities.task import Task
from ..entities.tasklist import TaskList


class TaskService(object):
    def __init__(self, requester):
        self.requester = requester

    def getTasks(self, card_or_cardcommonId, taskList_or_Id=None):
        from ..entities.tasklist import TaskList

        cardCommonId = card_or_cardcommonId
        if isinstance(card_or_cardcommonId, Card):
            cardCommonId = card_or_cardcommonId.cardCommonId

        tasklistId = taskList_or_Id
        if isinstance(taskList_or_Id, TaskList):
            tasklistId = taskList_or_Id.taskListId

        tasksJson = self.requester.getTasks(cardCommonId, tasklistId)
        tasks = []
        for taskJson in tasksJson['entities']:
            tasks.append(Task(taskJson, self.requester))
        return tasks

    def getTask(self, taskId):
        taskJson = self.requester.getTaskBy(taskId)
        task = Task(taskJson, self.requester)
        return task

    def createTask(self, taskList_or_Id, name, position=None, completed=None):
        tasklistId = taskList_or_Id
        if isinstance(taskList_or_Id, TaskList):
            tasklistId = taskList_or_Id.taskListId

        taskJson = self.requester.createTask(tasklistId, name, position, completed)
        task = Task(taskJson, self.requester)
        return task
