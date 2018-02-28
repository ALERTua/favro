#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class TaskList(object):
    def __init__(self, json, requester):
        self.requester = requester
        self.taskListId = json.get('taskListId', None)
        self.cardCommonId = json.get('cardCommonId', None)
        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)
        self.position = json.get('position', None)

    def __eq__(self, other):
        return self.taskListId == other.taskListId

    def __hash__(self):
        return hash(self.taskListId)

    def update(self, name=None, position=None):
        taskListJson = self.requester.updateTaskList(self.taskListId, name, position)
        taskList = TaskList(taskListJson, self.requester)
        return taskList

    def deleteTaskList(self):
        return self.requester.deleteTaskList(self.taskListId)
