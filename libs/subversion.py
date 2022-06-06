# -*- coding:utf-8 -*-
'''
Created on 6.06.2018 г.

@author: dedal
'''
import pysvn
import os


class SubVersion():
    def __init__(self, folder, url, user=None, passwd=None):
        self.user = user
        self.passwd = passwd
        self.folder = folder
        self.svn = url
        self.client = pysvn.Client()

        def callback_get_login(realm, username, may_save):
            name = self.user
            password = self.passwd
            return True, name, password, False

        if self.user != None:
            self.client.callback_get_login = callback_get_login

    def checkout(self):
        rev = self.client.checkout(self.svn, self.folder)
        return rev.number

    def info(self):
        return self.client.info(self.folder).revision.number

    def update(self, rev=None):
        if rev == None:
            rev = self.client.update(self.folder)
        else:
            self.client.switch(path=self.folder, url=self.svn,recurse=True,
                              revision=pysvn.Revision(kind=pysvn.opt_revision_kind.number, number=rev),
                                )
        return self.info()

    def commit(self, comment, folder=None):
        if folder == None:
            return self.client.checkin([self.folder], comment)
        else:
            return self.client.checkin([folder], comment)

    def revert(self):
        self.client.revert(self.folder)
        return True

    def add(self, new_file):
        return self.client.add(new_file)




