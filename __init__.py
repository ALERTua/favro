#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from .services.requester import Requester
from .services.cards import CardService
from .services.collections import CollectionService
from .services.columns import ColumnService
from .services.customFields import CustomFieldService
from .services.organizations import OrganizationService
from .services.tags import TagService
from .services.tasks import TaskService
from .services.tasklists import TaskListService
from .services.users import UserService
from .services.widgets import WidgetService


class Favro(object):
    def __init__(self, username, token, organizationId):
        self.requester = Requester(username, token, organizationId)

        self.cards = CardService(self.requester)
        self.collections = CollectionService(self.requester)
        self.columns = ColumnService(self.requester)
        self.customFields = CustomFieldService(self.requester)
        self.organizations = OrganizationService(self.requester)
        self.tags = TagService(self.requester)
        self.tasks = TaskService(self.requester)
        self.taskLists = TaskListService(self.requester)
        self.users = UserService(self.requester)
        self.widgets = WidgetService(self.requester)
