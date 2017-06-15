# -*- coding:utf-8 -*-
from AccessToDB import AccessToMongoDB
import sys
from bson.objectid import ObjectId

reload(sys)
sys.setdefaultencoding("utf-8")

obj = AccessToMongoDB()
# pro = obj.GeneralInterface("projects", "metatongue")
# doc = obj.GeneralInterface("samples", "TCM_38", "均称型")
# doc1 = obj.GetSamplesInfo("BMI", 23)
# print pro
# print doc
# for ddd in doc1:
#     print ddd
#     pass
#'MetaTongueProject'
# docs = obj.GeneralInterface(
#     "samples", "MetaTongueProject", "samples", "BMI", 23)
# print docs

# dictionary = [{"name": "steven1", "realname": "测试11", "age": 25},
#               {"name": "steven2", "realname": "测试12", "age": 26},
#               {"name": "steven1", "realname": "测试13", "age": 23}]
# obj.GeneralInterface("write_document", "my_test",  "biology_test", dictionary)

print obj.GeneralInterface("drop", "testCreate", "not_liuhe")
# obj.GeneralInterface("create", "test_Crea_te", "not_liuhe", {'Projects':'test_Crea_te', 'creator':'not_liuhe'})



# temp = obj.GetProjectInfo('metatongue')
# print temp

# obj_id = ObjectId('5418356d419a73b876d6a5e5')
# print obj_id
# temp2 = obj.GeneralInterface("samples", "_id", obj_id)
# print temp2
