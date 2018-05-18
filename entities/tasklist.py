#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester


class TaskList(object):
    def __init__(self, json, requester):
        self._requester = requester  # type: Requester
        self.taskListId = json.get('taskListId', None)
        self.cardCommonId = json.get('cardCommonId', None)
        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)
        self.position = json.get('position', None)

        self._json = json

    def __eq__(self, other):
        if not isinstance(other, TaskList):
            return False
        return self.taskListId == other.taskListId

    def __hash__(self):
        return hash(self.taskListId)

    def update(self, name=None, position=None):
        # type: (str, int) -> TaskList
        taskListJson = self._requester.updateTaskList(self.taskListId, name, position)
        taskList = TaskList(taskListJson, self._requester)
        return taskList

    def delete(self):
        return self._requester.deleteTaskList(self.taskListId)

    def createTask(self, name, position=None, completed=None):
        # type: (str, int, bool) -> Task
        from .task import Task
        taskJson = self._requester.createTask(self.taskListId, name, position, completed)
        task = Task(taskJson, self._requester)
        return task
