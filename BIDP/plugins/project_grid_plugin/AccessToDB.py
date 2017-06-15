# -*- coding:utf-8 -*-
# class that can access to the mongoDB.
# get the description of projects and samples
# written by liuhe 2012011300
# created at 30/10/2014
# 功能：支持对数据库的访问，可以使用中文、数字以及ObjectId进行查询进行查询
# GeneralInterface()接口使用方法：
# GeneralInterface("projects", "metatongue")
# GeneralInterface("samples", "TCM_38", "均称型")
# GeneralInterface("samples", "BMI", 23)
# GeneralInterface(tag, database_name, collection_name,  "_id", obj_id) ##其中obj_id是一个ObjectId类
# 其中tag可选'projects', 'samples', 'projectLists', 'write'

import pymongo
import json
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId

reload(sys)
sys.setdefaultencoding("utf-8")


class AccessToMongoDB(object):
    """docstring for AccessToMongoDB"""
    #db_name = "MetaTongueProject"

    def __init__(self):
        super(AccessToMongoDB, self).__init__()
        #self.db_name = db_name
        self.client = MongoClient("localhost", 27017)
        #self.dataBase = self.client[db_name]

    def GetProjectInfo(self, database_name, collection_name, project_name):
        dataBase = self.client[database_name]
        collection = dataBase[collection_name]
        info_list = collection.find({"name": project_name})
        dict_temp = []
        dictionary = {}
        for document in info_list:
            dictionary['createDate'] = str(document['createDate']).decode()
            dictionary['description'] = str(document['description']).decode()
            dictionary['name'] = str(document['name']).decode()
        dict_temp.append(dictionary)
        return dict_temp

    def GetSamplesInfo(self,  database_name, collection_name, sample_filter_key="", sample_filter_value=""):
        dataBase = self.client[database_name]
        collection = dataBase[collection_name]

        if sample_filter_key == "":
            temp_list = collection.find()
        else:
            temp_list = collection.find({sample_filter_key: sample_filter_value})
        dictionary = []
        for document in temp_list:
            dictionary.append(document)
            pass
        return dictionary

    def GetProjectList(self, database_name, collection_name):
        my_dbname = database_name  ##"projectLists"
        my_db = self.client[my_dbname]
        collection = my_db[collection_name]  ##"projectInfo"
        projectsInfo = collection.find()
        dictionary = []
        for doc in projectsInfo:
            dictionary.append(doc)
        return dictionary

    def GeneralInterface(self, tag, database_name, collection_name, req1="", req2=""):
        if tag == 'projects':
            return self.GetProjectInfo(database_name, collection_name, req1)
        elif tag == 'samples':
            return self.GetSamplesInfo(database_name, collection_name, req1, req2)
        elif tag == 'projectLists':
            return self.GetProjectList(database_name, collection_name)
        elif tag == 'write':
            self.writeToDB(database_name, collection_name, req1, req2)

    def writeToDB(self, db_name, collection_name, key, value):
        my_dbname = db_name
        my_db = self.client[my_dbname]
        collection = my_db[collection_name]
        collection.insert({key: value})
        pass
