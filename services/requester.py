#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
import requests
from requests.auth import HTTPBasicAuth


class Requester(object):
    def __init__(self, username, token, organizationId):
        self.authHeader = HTTPBasicAuth(username, token)
        self.organization = {'organizationId': organizationId}
        self.favroBaseUrl = 'https://favro.com/api/v1/'
        self.requests = requests

        self.all_tags = None
        self.organizations = None

    def _get(self, url, **kwargs):
        return self._request('get', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('post', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('put', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('delete', url, **kwargs)

    def _request(self, method, url, **kwargs):
        url = self.favroBaseUrl + url
        kwargs.update({'auth': self.authHeader, 'headers': self.organization})

        methods = {'get': self.requests.get,
                   'post': self.requests.post,
                   'put': self.requests.put,
                   'delete': self.requests.delete}

        # import json as js
        # data = None
        # if 'data' in kwargs:
        #     data = js.dumps(kwargs['data'])
        #     kwargs.pop('data', None)
        #
        # r = methods[method](url, json=data, **kwargs)
        r = methods[method](url, **kwargs)

        rateLimitRemaining = int(r.headers.get('X-RateLimit-Remaining', 100))
        rateLimit = int(r.headers.get('X-RateLimit-Limit', 100))
        rateLimitReset = r.headers.get('X-RateLimit-Reset', None)
        output = r.json()

        if r.status_code == 429:
            raise Exception("[%s] Rate limit exceeded: %s/%s until %s" % (r.status_code, rateLimitRemaining,
                                                                          rateLimit, rateLimitReset))

        if rateLimitRemaining % 100 == 0:
            print("Favro Rate limits: %s/%s" % (rateLimitRemaining, rateLimit))

        if not r.ok:
            raise Exception("(%s/%s) Request returned code %s: %s in %s" % (rateLimitRemaining, rateLimit,
                                                                            r.status_code, output.get('message', ''),
                                                                            r.request.url))

        if method == 'delete':
            return output

        page = output.get('page', 0)
        pages = output.get('pages', 0)
        requestId = r.headers.get('X-Favro-Backend-Identifier', None)
        while page < pages - 1:
            params = kwargs.get('params', {})
            params.update({'requestId': requestId, 'page': page + 1})
            pagedrequest = methods[method](url, **kwargs)
            pagedrequestjson = pagedrequest.json()
            page = pagedrequestjson.get('page', 0)
            newpages = pagedrequestjson.get('pages', 0)
            if newpages != pages:
                raise Exception("pages quantity mismatch")
            requestId = pagedrequest.headers.get('X-Favro-Backend-Identifier', None)
            entities = pagedrequestjson.get('entities', [])
            output['entities'] += entities

        return output

# + Organizations
    def getOrganizations(self):
        if self.organizations is None:
            r = self.requests.get(self.favroBaseUrl + 'organizations', auth=self.authHeader)
            if r.status_code != 200:
                raise Exception("Get organizations request returned " + str(r.status_code) + " code")
            organizationsJson = r.json()
            self.organizations = []
            for organizationJson in organizationsJson['entities']:
                self.organizations.append(organizationJson)

        return self.organizations
# - Organizations

# + Collections
    def getCollections(self):
        """

        :rtype:
        """
        return self._get('collections')

    def getCollection(self, collectionId):
        return self._get('collections/' + collectionId)
# - Collections

# + Widgets
    def getWidgets(self, collectionId):
        data = {'collectionId': collectionId}
        return self._get('widgets', data=data)

    def getWidget(self, widgetCommonId):
        return self._get('widgets/' + widgetCommonId)

    def createWidget(self, widgetName, collectionId):
        data = {'collectionId': collectionId, 'name': widgetName, 'type': 'board'}
        return self._post('widgets', data=data)
# - Widgets

# + Columns
    def getColumns(self, widgetCommonId):
        params = {'widgetCommonId': widgetCommonId}
        return self._get('columns', params=params)

    def getColumn(self, columnId):
        return self._get('columns/' + columnId)

    def createColumn(self, widgetCommonId, name, position=None):
        data = {'widgetCommonId': widgetCommonId, 'name': name}
        if position is not None:
            data['position'] = position
        return self._post('columns', data=data)

    def updateColumn(self, columnId, new_name=None, new_position=None):
        data = {}
        if new_name is not None:
            data['name'] = new_name
        if new_position is not None:
            data['position'] = new_position
        if not bool(data):
            print("updateColumn received no data")
            return
        return self._put('columns/' + columnId, data=data)
# - Columns

# + Cards
    def getCardsByFilters(self, filters=None, unique=False, todoListOnly=False):
        """
        :type filters: dict
        :type unique: bool
        :type todoListOnly: bool
        """
        if filters is None:
            filters = {}
        if unique:
            filters['unique'] = str(unique).lower()

        if todoListOnly:
            filters['todoList'] = str(todoListOnly).lower()

        return self._get('cards', params=filters)

    def getCard(self, cardId):
        return self._get('cards/' + cardId)

    def createCard(self, **kwargs):
        return self._post('cards', data=kwargs)

    def updateCard(self, cardId, data):
        return self._put('cards/' + cardId, data=data)

    def deleteCard(self, cardId, everywhere=False):
        params = {'everywhere': True} if everywhere else None
        return self._delete('cards/' + cardId, params=params)
# - Cards

# + Tags
    def getTags(self, name=None):
        data = {'name': name} if name is not None else None
        return self._get('tags', data=data)

    def getTag(self, tagId):
        return self._get('tags/' + tagId)

    def createTag(self, name, color=None):
        data = {'name': name}

        if color is not None:
            data['color'] = color

        return self._post('tags', data=data)

    def updateTag(self, tagId, name=None, color=None):
        data = {'name': name}

        if color is not None:
            data['color'] = color

        return self._put('tags/' + tagId, data=data)

    def deleteTag(self, tagId):
        return self._delete('tags/' + tagId)

    def getTagsDict(self):
        """

        :rtype: dict
        """
        from ..entities.tag import Tag

        if self.all_tags is None:
            all_tags_json = self.getTags()
            self.all_tags = {}
            for tagJson in all_tags_json['entities']:
                tag = Tag(tagJson, self)
                self.all_tags[tag.name] = tag.tagId
        return self.all_tags
# - Tags

# + Tasks
    def getTasks(self, cardCommonId, taskListId=None):
        params = {'cardCommonId': cardCommonId}
        if taskListId is not None:
            params['taskListId'] = taskListId
        return self._get('tasks', params=params)

    def getTask(self, taskId):
        return self._get('tasks/' + taskId)

    def createTask(self, taskListId, name, position=None, completed=None):
        data = {'taskListId': taskListId, 'name': name}
        if position is not None:
            data['position'] = position
        if completed is not None:
            data['completed'] = completed
        return self._post('tasks', data=data)

    def updateTask(self, taskId, name=None, position=None, completed=None):
        data = {}
        if name is not None:
            data['name'] = name
        if position is not None:
            data['position'] = position
        if completed is not None:
            data['completed'] = completed
        return self._put('tasks/' + taskId, data=data)

    def deleteTask(self, taskId):
        return self._delete('tasks/' + taskId)
# - Tasks

# + TaskLists
    def getTaskLists(self, cardCommonId):
        params = {'cardCommonId': cardCommonId}
        return self._get('tasklists', params=params)

    def getTaskList(self, taskListId):
        return self._get('tasklists/' + taskListId)

    def createTaskList(self, cardCommonId, name, position=None, tasks=None):
        # type: (str, str, int, list) -> object
        data = {'cardCommonId': cardCommonId, 'name': name}
        if position is not None:
            data['position'] = position
        if tasks is not None:
            data['tasks'] = tasks
        return self._post('tasklists', data=data)

    def updateTaskList(self, taskListId, name=None, position=None):
        data = {}
        if name is not None:
            data['name'] = name
        if position is not None:
            data['position'] = position
        return self._put('tasklists/' + taskListId, data=data)

    def deleteTaskList(self, taskListId):
        return self._delete('tasklists/' + taskListId)
# - TaskLists

# + Comments
    def addComment(self, cardCommonId, comment):
        data = {'cardCommonId': cardCommonId, 'comment': comment}
        output = self._post('comments', data=data)
        return output
# - Comments
