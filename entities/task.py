#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8


class Task(object):
    def __init__(self, json, requester):
        self.requester = requester
        self.taskId = json.get('taskId', None)
        self.taskListId = json.get('taskListId', None)
        self.cardCommonId = json.get('cardCommonId', None)
        self.organizationId = json.get('organizationId', None)
        self.name = json.get('name', None)
        self.completed = json.get('completed', None)
        self.position = json.get('position', None)

    def __eq__(self, other):
        return self.taskId == other.taskId

    def __hash__(self):
        return hash(self.taskId)

    def update(self, name=None, position=None, completed=None):
        taskJson = self.requester.updateTask(self.taskId, name, position, completed)
        task = Task(taskJson, self.requester)
        return task

    def deleteTask(self):
        return self.requester.deleteTask(self.taskId)
