#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from services.requester import Requester
from services.collection import CollectionService
from services.widget import WidgetService
from services.tasklist import TaskListService
from services.task import TaskService
from services.column import ColumnService
from services.tag import TagService
from services.card import CardService
from services.user import UserService


class Favro(object):
    def __init__(self, username, token, organizationId):
        self.requester = Requester(username, token, organizationId)

        self.card = CardService(self.requester)
        self.collection = CollectionService(self.requester)
        self.column = ColumnService(self.requester)
        self.tag = TagService(self.requester)
        self.task = TaskService(self.requester)
        self.taskList = TaskListService(self.requester)
        self.user = UserService(self.requester)
        self.widget = WidgetService(self.requester)
