#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.collection import Collection


class CollectionService(object):
    def __init__(self, requester):
        self.__requester = requester

    def __getCollectionIdFromName(self, collection_name):
        collectionsJson = self.__requester.getCollections()
        for collectionJson in collectionsJson['entities']:
            collection = Collection(collectionJson, self.__requester)
            if collection_name in collection.name:
                return collection.collectionId

    def getCollectionByName(self, name):
        collectionId = self.__getCollectionIdFromName(name)
        return self.getCollection(collectionId)

    def getCollection(self, collectionId):
        collectionJson = self.__requester.getCollection(collectionId)
        collection = Collection(collectionJson, self.__requester)
        return collection

    def getCollections(self):
        collectionsJson = self.__requester.getCollections()
        collections = []
        for collectionJson in collectionsJson['entities']:
            collections.append(Collection(collectionJson, self.__requester))
        return collections


