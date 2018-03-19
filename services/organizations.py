#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from ..entities.organization import Organization


class OrganizationService(object):
    def __init__(self, requester):
        self.__requester = requester

    def getOrganizations(self):
        """
        :rtype: list of Organization
        """
        organizationsJson = self.__requester.getOrganizations()
        organizations = []
        for organizationJson in organizationsJson:
            organizations.append(Organization(organizationJson, self.__requester))
        return organizations

    def getOrganizationByName(self, name):
        """
        :rtype: Organization
        """
        organizations = self.getOrganizations()
        for organization in organizations:
            if organization.name == name:
                return organization
        return None

    def getOrganizationById(self, organizationId):
        """
        :rtype: Organization
        """
        organizations = self.getOrganizations()
        for organization in organizations:
            if organization.organizationId == organizationId:
                return organization
        return None
