#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.tasklist import TaskList


class TaskListService(object):
    def __init__(self, requester):
        self.__requester = requester

    def getTaskList(self, taskListId):
        # type: (str) -> TaskList
        taskListJson = self.__requester.getTaskList(taskListId)
        taskList = TaskList(taskListJson, self.__requester)
        return taskList
