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
# GeneralInterface(tag, database_name, collection_name,  "_id", obj_id)
# 其中obj_id是一个ObjectId类
# 其中tag可选'projects', 'samples', 'projectLists', 'write', 'write_document',
# 'drop'

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

# 获取工程信息，包括工程名，创建时间，工程描述
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

# 获取某个工程中的采集的样例的信息
    def GetSamplesInfo(self, database_name, collection_name, key="", value=""):
        dataBase = self.client[database_name]
        collection = dataBase[collection_name]

        if key == "":
            temp_list = collection.find()
        else:
            temp_list = collection.find(
                {key: value})
        dictionary = []
        for document in temp_list:
            dictionary.append(document)
            pass
        return dictionary

# 获取所有工程的基本信息，对应的mongodb中的数据库是projectLists。
    def GetProjectList(self, database_name, collection_name):
        my_dbname = database_name  # "projectLists"
        my_db = self.client[my_dbname]
        collection = my_db[collection_name]  # "projectInfo"
        projectsInfo = collection.find()
        dictionary = []
        for doc in projectsInfo:
            dictionary.append(doc)
        return dictionary

# 通用接口，根据不同的tag来区分不同的操作。
    def GeneralInterface(self, tag, database_name, collection_name, req1="", req2=""):
        if tag == 'projects':
            return self.GetProjectInfo(database_name, collection_name, req1)
        elif tag == 'samples':
            return self.GetSamplesInfo(database_name, collection_name, req1, req2)
        elif tag == 'projectLists':
            return self.GetProjectList(database_name, collection_name)
        elif tag == 'write':  # 写入一个键值对
            self.writeToDB(database_name, collection_name, req1, req2)
        elif tag == 'write_document':  # 写入一个list，该list中包含多个document
            self.writeDocToDB(database_name, collection_name, req1)
        elif tag == 'drop':
            return self.dropProject(database_name, collection_name)
        elif tag == 'create':
            return self.createProject(database_name, collection_name, req1)
        elif tag == 'check':
            return self.inProjectLists(database_name, collection_name)
        elif tag == 'delete_doc':
            self.deleteADoc(database_name, collection_name, req1, req2)

# 向数据库中的写入一个键值对
    def writeToDB(self, db_name, collection_name, key, value):
        my_dbname = db_name
        my_db = self.client[my_dbname]
        collection = my_db[collection_name]
        collection.insert({key: value})
        pass

# 向数据库中写入一个list，即可以以json格式输入
    def writeDocToDB(self, db_name, collection_name, dictionary):
        my_db = self.client[db_name]
        collection = my_db[collection_name]
        collection.insert(dictionary)
        pass

# 删除一个project。首先判断该project是否为creator_name用户创建的
# 若是，则可以将该数据库进行删除，否则返回False告知网页不能删除。
    def dropProject(self, pro_name, userInfo):
        db_proList = self.client['projectLists']
        collection_proList = db_proList['projectInfo']
        item = collection_proList.find({'Projects': pro_name})

        flag = False
        for it in item:
            if it['creator'] == userInfo.username or userInfo.is_superuser:
                flag = True
                collection_proList.remove(it)  # 将projectLists数据库中的相应条目删除
                pass

        if not flag:
            return False  # 删除失败
            pass

        db_name = pro_name + "Project"
        return self.dropDatabase(db_name)
        pass

# 删除数据库，返回值是TRUE和FALSE。若成功删除（要删除的数据库存在）则返回TRUE，否则返回FALSE。
    def dropDatabase(self, db_name):
        dbNames = self.getDatabaseNames()
        for items in dbNames:
            if items == db_name:
                self.client.drop_database(db_name)
                return True
                pass
        return False
        pass

# 删除samples中具有指定键值的数据行
    def deleteADoc(self, project_name, key, value, userInfo):
        temp = self.inProjectLists(project_name, userInfo)
        if temp == 0 or temp == 2:
            return
            pass

        # print 'hahahahaha'
        name = project_name + 'Project'
        my_db = self.client[name]
        my_col = my_db['samples']
        items = my_col.find({key: value})
        for it in items:
            my_col.remove(it)
            pass
        pass

# 返回值是一个list，因此访问的时候要用for循环进行访问
    def getDatabaseNames(self):
        return self.client.database_names()
        pass

# 返回值是一个list，要用for循环进行访问
    def getCollectionNames(self, db_name):
        my_db = self.client[db_name]
        return my_db.collection_names()
        pass

# 返回值为0：不存在名为project_name的工程，1：存在名为project_name且创建者为creator的工程
# 2：存在名为project_name但创建者不是creator
    def inProjectLists(self, project_name, userInfo):
        db_proList = self.client['projectLists']
        collection_proList = db_proList['projectInfo']
        items = collection_proList.find({'Projects': project_name})
        temp_doc = []

        for it in items:
            if it['creator'] == userInfo.username or userInfo.is_superuser:
                return 1
                pass
            temp_doc.append(it)
            pass
        if len(temp_doc) == 0:
            return 0
            pass
        return 2
        pass

# 返回值为1,2,3等，分别对应<新工程可以创建><同名工程，但是creator为同一人，可以覆盖><同名工程，创建被拒绝>
# 该函数在projectLists库中创建了一个新的工程信息，而创建新工程所需的数据库需要调用writeDocToDB接口进行实现
    def createProject(self, project_name, project_info, userInfo):
        db_proList = self.client['projectLists']
        collection_proList = db_proList['projectInfo']

        temp = self.inProjectLists(project_name, userInfo)

        if temp == 0:
            # 将新创建的工程信息加入到projectLists数据库中
            collection_proList.insert(project_info)
            # 给该工程加入一条属性creator = creator_name
            collection_proList.update(
                {'Projects': project_name}, {'$set': {'creator': userInfo.username}})
            return 1
            pass
        elif temp == 1:
            # 对于同一用户创建的同名工程，需要先把原数据库删掉
            collection_proList.update({'Projects': project_name}, project_info)
            collection_proList.update(
                {'Projects': project_name}, {'$set': {'creator': userInfo.username}})
            database_name = project_name + "Project"
            self.dropDatabase(database_name)
            return 2
            pass
        else:
            return 3
            pass

        pass
