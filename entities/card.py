#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..services.requester import Requester
from .tasklist import TaskList


class Card(object):
    def __init__(self, json, requester):
        self._json = json
        self._requester = requester  # type: Requester

        _message = json.get('message', None)  # type: str
        if _message is not None:
            raise Exception("Error initiating %s class: %s" % (self.__class__.__name__, _message))

        self.archived = json.get('archived')  # type: bool

        self.assignments = []  # type: list
        from .user import User
        for user in json.get('assignments', []):
            self.assignments.append(User(user, self._requester))

        self.attachments = []  # type: list
        for attachment in json.get('attachments', []):
            self.attachments.append(attachment)
            # todo: Attachment()

        self.cardCommonId = json.get('cardCommonId')  # type: str
        self.cardId = json.get('cardId')  # type: str
        self.columnId = json.get('columnId')  # type: str

        self.__customFields = None
        self.customFieldsValuesDict = {}
        for customField in json.get('customFields', {}):
            _id = customField.get('customFieldId', None)
            _value = customField.get('value', None) or customField.get('total', None)
            self.customFieldsValuesDict[_id] = _value

        self.detailedDescription = json.get('detailedDescription', None)  # type: str
        self.dueDate = json.get('dueDate', None)
        self.isLane = json.get('isLane')  # type: bool
        self.name = json.get('name')  # type: str
        self.numComments = json.get('numComments', None)  # type: int
        self.organizationId = json.get('organizationId')  # type: str
        self.parentCardId = json.get('parentCardId', None)  # type: str
        self.position = json.get('position')  # type: float
        self.sequentialId = json.get('sequentialId', None)  # type: str

        self.tagsIds = []
        for tag in json.get('tags', []):
            self.tagsIds.append(tag)

        self.tasksTotal = json.get('tasksTotal', None)  # type: int
        self.tasksDone = json.get('tasksDone', None)  # type: int
        self.timeOnBoard = json.get('timeOnBoard', None)  # todo: namedtuple?
        self.timeOnColumns = json.get('timeOnColumns', None)  # todo: namedtuple?
        self.todoListUserId = json.get('todoListUserId', None)  # type: str
        self.todoListCompleted = json.get('todoListCompleted', None)  # type: str
        self.widgetCommonId = json.get('widgetCommonId')  # type: str

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.cardCommonId == other.cardCommonId

    def __hash__(self):
        return hash(self.cardCommonId)

    def __str__(self):
        return self.name

    @property
    def widget_name(self):
        return self._requester.getWidget(self.widgetCommonId)['name']

    @property
    def customFields(self):
        """

        :rtype: list of CustomField
        """
        if self.__customFields is None:
            from ..services.customFields import CustomFieldService
            customFieldService = CustomFieldService(self._requester)
            _customFieldsList = []
            for customFieldId, customFieldValue in self.customFieldsValuesDict.items():
                _new_customField = customFieldService.getCustomField(customFieldId)
                if _new_customField in _customFieldsList:
                    continue
                _new_customField.value = customFieldValue
                _customFieldsList.append(_new_customField)
            self.__customFields = _customFieldsList
        return self.__customFields

    @property
    def tagNames(self):
        """

        :rtype: list of str
        """
        all_tags = self._requester.getTagsDict()
        tag_names = [name for name, _id in all_tags.items() if _id in self.tagsIds]
        return tag_names

    def getCustomFieldByFilter(self, customFieldName, customFieldType):
        for customField in self.customFields:
            if customField.name == customFieldName and customField.type in customFieldType:
                return customField
        return None

    def setCustomFieldValue(self, customField, value):
        _customField_json = {'customFields': [{'customFieldId': customField.customFieldId, 'value': value}]}

        from .customField import CustomFieldType
        if customField.type == CustomFieldType.NUMBER:
            _customField_json = {'customFields': [{'customFieldId': customField.customFieldId, 'total': value}]}

        return self.update(json=_customField_json)

    def addComment(self, comment):
        return self._requester.addComment(self.cardCommonId, comment)

    def rename(self, new_name):
        return self.update(name=new_name)

    def modify_description(self, new_description):
        return self.update(detailedDescription=new_description)

    def move(self, column_or_Id=None, widget_or_Id=None, position=None):
        from .column import Column
        from .widget import Widget
        if isinstance(column_or_Id, Column):
            column_or_Id = column_or_Id.columnId

        if self.columnId == column_or_Id and widget_or_Id is None:
            return self

        if widget_or_Id is None:
            widget_or_Id = self.widgetCommonId
        else:
            if isinstance(widget_or_Id, Widget):
                widget_or_Id = widget_or_Id.widgetCommonId

        return self.update(widgetCommonId=widget_or_Id, column_or_Id=column_or_Id, position=position, dragMode='move')

    def copy(self, column_or_Id=None, widgetCommonId=None, parentCardId=None):
        _widgetCommonId = self.widgetCommonId
        if widgetCommonId is not None:
            _widgetCommonId = widgetCommonId
        output = self.update(widgetCommonId=_widgetCommonId, column_or_Id=column_or_Id, parentCardId=parentCardId, dragMode='commit')
        return output

    def reposition(self, position):
        """

        :type position: int
        """
        if position == self.position:
            return
        output = self._requester._put('cards/' + self.cardId, json={'position': position})
        self.position = position

    def archive(self, value=True):
        if value == self.archived:
            return
        output = self._requester._put('cards/' + self.cardId, json={'archive': value})
        self.archived = value

    def unarchive(self):
        return self.archive(value=False)

    def removeAllTags(self):
        return self.update(removeTagIds=self.tagsIds)

    def update(self, name=None, detailedDescription=None, widgetCommonId=None,
               laneId=None, column_or_Id=None, parentCardId=None, dragMode=None, position=None,
               addAssignmentIds=None, removeAssignmentIds=None, addTags=None, addTagIds=None,
               removeTags=None, removeTagIds=None, startDate=None, dueDate=None, addTasklists=None,
               removeAttachments=None, customFields=None, **kwargs):
        """
        :rtype: Card
        """

        data = {}

        if name is not None:
            data['name'] = name

        if detailedDescription is not None:
            # *italic*, **bold**, ```code block```, [Link](“http://localhost”)
            data['detailedDescription'] = detailedDescription

        if widgetCommonId is not None:
            data['widgetCommonId'] = widgetCommonId

        if laneId is not None:
            data['laneId'] = laneId

        if column_or_Id is not None:
            from .column import Column
            columnId = column_or_Id
            if isinstance(column_or_Id, Column):
                columnId = column_or_Id.columnId
            data['columnId'] = columnId

        if parentCardId is not None:
            data['parentCardId'] = parentCardId

        dragModes = ['commit', 'move']
        if dragMode is not None:
            if dragMode not in dragModes:
                raise Exception("updateCard: dragMode %s is not in acceptable %s" % (str(dragMode), dragModes))
            data['dragMode'] = dragMode

        if position is not None:
            data['position'] = int(position)

        if addAssignmentIds is not None:
            data['addAssignmentIds'] = addAssignmentIds

        if removeAssignmentIds is not None:
            data['removeAssignmentIds'] = removeAssignmentIds

        if addTags is not None:
            data['addTags'] = addTags

        if addTagIds is not None:
            data['addTagIds'] = addTagIds

        if removeTags is not None:
            data['removeTags'] = removeTags

        if removeTagIds is not None:
            data['removeTagIds'] = removeTagIds

        if startDate is not None:
            data['startDate'] = startDate

        if dueDate is not None:
            data['dueDate'] = dueDate

        if addTasklists is not None:
            from .tasklist import TaskList

            for task in addTasklists:
                if not isinstance(task, TaskList):
                    raise Exception("updateCard: addTasklists must contain only TaskList objects")

            data['addTasklists'] = addTasklists

        if removeAttachments is not None:
            data['removeAttachments'] = removeAttachments

        if customFields is not None:
            data['customFields'] = customFields

        cardJson = self._requester.updateCard(self.cardId, data, **kwargs)
        card = Card(cardJson, self._requester)
        return card

    def delete(self, everywhere=False):
        """
        :rtype: list
        """
        cardJson = self._requester.deleteCard(self.cardId, everywhere)
        deleted_card_ids = list(cardJson)
        return deleted_card_ids

    def addTagsByName(self, tags, mode_set=False, all_tags=None):
        """

        :param all_tags: dict
        :param mode_set: bool
        :type tags: list[str]
        """
        all_tags = all_tags or self._requester.getTagsDict()
        tagsIds = [tagId for tagName, tagId in all_tags.items() if tagName in tags]
        addTagIds = [tagId for tagId in tagsIds if tagId not in self.tagsIds]
        if len(addTagIds) == 1:
            addTagIds.append(addTagIds[0])
            # funny, huh?

        removeTagIds = None
        if mode_set is True:
            removeTagIds = [tagId for tagId in self.tagsIds if tagId not in tagsIds]
            if len(removeTagIds) == 1:
                removeTagIds.append(removeTagIds[0])
                # funny, huh?

        if any(addTagIds) or any(removeTagIds):
            self.update(addTagIds=addTagIds, removeTagIds=removeTagIds)

    def getTaskLists(self):
        """

        :rtype: list of TaskList
        """
        taskListsJson = self._requester.getTaskLists(self.cardCommonId)
        taskLists = []
        for taskListJson in taskListsJson.get('entities', {}):
            tasklist = TaskList(taskListJson, self._requester)
            taskLists.append(tasklist)

        return list(set(taskLists))

    def createTaskList(self, name, position=None, tasks=None):
        """

        :param name: string name
        :param position: int position
        :param tasks: https://favro.com/developer/#create-a-task-list List of Task dicts, containing 'name' string and 'completed' boolean
        :return: TaskList
        """
        taskListJson = self._requester.createTaskList(self.cardCommonId, name, position, tasks)
        taskList = TaskList(taskListJson, self._requester)
        return taskList

    def getTasks(self, taskList_or_Id=None):
        """

        :rtype: list of Task
        """
        from .task import Task
        tasklistId = taskList_or_Id
        if isinstance(taskList_or_Id, TaskList):
            tasklistId = taskList_or_Id.taskListId

        tasksJson = self._requester.getTasks(self.cardCommonId, tasklistId)
        tasks = []
        for taskJson in tasksJson['entities']:
            tasks.append(Task(taskJson, self._requester))
        return tasks
