#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.collection import Collection


class CollectionService(object):
    def __init__(self, requester):
        self.__requester = requester

    def getCollectionByName(self, name):
        """

        :rtype: Collection
        """
        collections = self.getCollections()
        for collection in collections:
            if collection.name == name:
                return collection
        raise Exception("There's no such collection as %s" % name)

    def getCollection(self, collectionId):
        """

        :rtype: Collection
        """
        collectionJson = self.__requester.getCollection(collectionId)
        collection = Collection(collectionJson, self.__requester)
        return collection

    def getCollections(self):
        """

        :rtype: list of Collection
        """
        collectionsJson = self.__requester.getCollections()
        collections = []
        for collectionJson in collectionsJson['entities']:
            collections.append(Collection(collectionJson, self.__requester))
        return collections
