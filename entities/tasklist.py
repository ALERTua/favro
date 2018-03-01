#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from .task import Task


class TaskList(object):
    def __init__(self, json, requester):
        self.__requester = requester
        self.taskListId = json.get('taskListId', None)
        self.cardCommonId = json.get('cardCommonId', None)
        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)
        self.position = json.get('position', None)

        self._json = json

    def __eq__(self, other):
        return self.taskListId == other.taskListId

    def __hash__(self):
        return hash(self.taskListId)

    def update(self, name=None, position=None):
        # type: (str, int) -> TaskList
        taskListJson = self.__requester.updateTaskList(self.taskListId, name, position)
        taskList = TaskList(taskListJson, self.__requester)
        return taskList

    def delete(self):
        return self.__requester.deleteTaskList(self.taskListId)

    def createTask(self, name, position=None, completed=None):
        # type: (str, int, bool) -> Task
        taskJson = self.__requester.createTask(self.taskListId, name, position, completed)
        task = Task(taskJson, self.__requester)
        return task
