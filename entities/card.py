#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from .tasklist import TaskList
from .task import Task
from .column import Column
from .customField import CustomField, CustomFieldType


class Card(object):
    def __init__(self, json, requester):
        self.__requester = requester

        from .user import User

        _message = json.get('message', None)
        if _message is not None:
            raise Exception("Error initiating %s class: %s" % (self.__name__, _message))

        self.cardId = json.get('cardId', None)
        self.organizationId = json.get('organizationId', None)
        self.widgetCommonId = json.get('widgetCommonId', None)
        self.todoListUserId = json.get('todoListUserId', None)
        self.todoListCompleted = json.get('todoListCompleted', None)
        self.columnId = json.get('columnId', None)
        self.laneId = json.get('laneId', None)
        self.parentCardId = json.get('parentCardId', None)
        self.isLane = json.get('isLane', None)
        self.archived = json.get('archived', None)
        self.position = json.get('position', None)
        self.cardCommonId = json.get('cardCommonId', None)
        self.name = json.get('name', None)
        self.detailedDescription = json.get('detailedDescription', None)

        self.tagsIds = []
        for tag in json.get('tags', []):
            self.tagsIds.append(tag)

        self.sequentialId = json.get('sequentialId', None)
        self.startDate = json.get('startDate', None)
        self.dueDate = json.get('dueDate', None)

        self.assignments = []
        for user in json.get('assignments', []):
            self.assignments.append(User(user, self.__requester))

        self.numComments = json.get('numComments', None)
        self.tasksTotal = json.get('tasksTotal', None)
        self.tasksDone = json.get('tasksDone', None)

        self.attachments = []
        for attachment in json.get('attachments', []):
            self.attachments.append(attachment)
            # todo: Attachment()

        self.customFieldsValuesDict = {}
        for customField in json.get('customFields', {}):
            _id = customField.get('customFieldId', None)
            _value = customField.get('value', None)
            self.customFieldsValuesDict[_id] = _value

        self.__customFields = None

        self._json = json

    def __eq__(self, other):
        return self.cardCommonId == other.cardCommonId

    def __hash__(self):
        return hash(self.cardCommonId)

    @property
    def customFields(self):
        """

        :rtype: list of CustomField
        """
        if self.__customFields is None:
            from ..services.customFields import CustomFieldService
            customFieldService = CustomFieldService(self.__requester)
            _customFieldsList = []
            for customFieldId, customFieldValue in self.customFieldsValuesDict.iteritems():
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
        all_tags = self.__requester.getTagsDict()
        tag_names = [name for name, _id in all_tags.iteritems() if _id in self.tagsIds]
        return tag_names

    def getCustomFieldByFilter(self, customFieldName, customFieldType):
        # type: (str, CustomFieldType) -> CustomField
        for customField in self.customFields:
            if customField.name == customFieldName and customField.type in customFieldType:
                return customField
        return None

    def setCustomFieldValue(self, customField, value):
        _customField_json = {'customFieldId': customField.customFieldId, 'value': value}
        return self.update(customFields=[_customField_json])

    def addComment(self, comment):
        return self.__requester.addComment(self.cardCommonId, comment)

    def rename(self, new_name):
        return self.update(name=new_name)

    def modify_description(self, new_description):
        return self.update(detailedDescription=new_description)

    def move(self, column_or_Id):
        _columnId = column_or_Id
        if isinstance(column_or_Id, Column):
            _columnId = column_or_Id.columnId
        if self.columnId == _columnId:
            return self

        return self.update(widgetCommonId=self.widgetCommonId, column_or_Id=column_or_Id,
                           dragMode='move')

    def copy(self, column_or_Id, widgetCommonId=None):
        _widgetCommonId = self.widgetCommonId
        if widgetCommonId is not None:
            _widgetCommonId = widgetCommonId
        return self.update(widgetCommonId=_widgetCommonId, column_or_Id=column_or_Id,
                           dragMode='commit')

    def removeAllTags(self):
        return self.__requester.updateCard(self.cardId, removeTagIds=self.tagsIds)

    def update(self, name=None, detailedDescription=None, widgetCommonId=None,
               laneId=None, column_or_Id=None, parentCardId=None, dragMode=None, position=None,
               addAssignmentIds=None, removeAssignmentIds=None, addTags=None, addTagIds=None,
               removeTags=None, removeTagIds=None, startDate=None, dueDate=None, addTasklists=None,
               removeAttachments=None, customFields=None):
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
            data['position'] = position

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

        cardJson = self.__requester.updateCard(self.cardId, data)
        card = Card(cardJson, self.__requester)
        return card

    def delete(self, everywhere=False):
        """
        :rtype: list
        """
        cardJson = self.__requester.deleteCard(self.cardId, everywhere)
        deleted_card_ids = list(cardJson)
        return deleted_card_ids

    def addTagsByName(self, tags, mode_set=False):
        if not isinstance(tags, list):
            raise Exception("addTagsByName: tags must be a list, not a %s" % type(tags))

        all_tags = self.__requester.getTagsDict()
        addTagIds = [all_tags.get(tag, None) for tag in tags if tag not in self.tagNames]
        if len(addTagIds) == 1:
            addTagIds.append(addTagIds[0])
            # funny, huh?

        removeTagIds = None
        if mode_set is True:
            removeTagIds = [tagId for tagId in self.tagsIds if tagId not in addTagIds]
            if len(removeTagIds) == 1:
                removeTagIds.append(removeTagIds[0])
                # funny, huh?

        if len(addTagIds) > 0:
            self.update(addTagIds=addTagIds, removeTagIds=removeTagIds)

    def getTaskLists(self):
        """

        :rtype: list of TaskList
        """
        taskListsJson = self.__requester.getTaskLists(self.cardCommonId)
        taskLists = []
        for taskListJson in taskListsJson.get('entities', {}):
            tasklist = TaskList(taskListJson, self.__requester)
            taskLists.append(tasklist)

        return list(set(taskLists))

    def createTaskList(self, name, position=None, tasks=None):
        """

        :param name: string name
        :param position: int position
        :param tasks: https://favro.com/developer/#create-a-task-list List of Task dicts, containing 'name' string and 'completed' boolean
        :return: TaskList
        """
        taskListJson = self.__requester.createTaskList(self.cardCommonId, name, position, tasks)
        taskList = TaskList(taskListJson, self.__requester)
        return taskList

    def getTasks(self, taskList_or_Id=None):
        """

        :rtype: list of Task
        """
        tasklistId = taskList_or_Id
        if isinstance(taskList_or_Id, TaskList):
            tasklistId = taskList_or_Id.taskListId

        tasksJson = self.__requester.getTasks(self.cardCommonId, tasklistId)
        tasks = []
        for taskJson in tasksJson['entities']:
            tasks.append(Task(taskJson, self.__requester))
        return tasks
