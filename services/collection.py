#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.collection import Collection


class CollectionService(object):
    def __init__(self, requester):
        self.requester = requester

    def getCollectionIdFromName(self, collection_name):
        collectionsJson = self.requester.getCollections()
        for collectionJson in collectionsJson['entities']:
            collection = Collection(collectionJson)
            if collection_name in collection.name:
                return collection.collectionId

    def getCollection(self, collectionId):
        collectionJson = self.requester.getCollection(collectionId)
        collection = Collection(collectionJson)
        return collection

    def getCollections(self):
        collectionsJson = self.requester.getCollections()
        collections = []
        for collectionJson in collectionsJson['entities']:
            collections.append(Collection(collectionJson))
        return collections

