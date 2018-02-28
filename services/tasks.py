#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.task import Task


class TaskService(object):
    def __init__(self, requester):
        self.__requester = requester

    def getTask(self, taskId):
        taskJson = self.__requester.getTaskBy(taskId)
        task = Task(taskJson, self.__requester)
        return task
