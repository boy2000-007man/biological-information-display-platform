1.Project list 中共5个project，详情见ProjectList.xls，用户只提供其中“MetaTongue project”项目中的样本数据；
2.MetaTongue Project共包括183个样本，样本的所有属性信息（即功能需求1.(b)中的表格的属性）包含在.json 和 .bson文件中；
3.183个样本中只提供样本名为“QH-01”和“QH-11”的分析结果，包含在“ExampleSampleAnalysisResult”的文件中；
4.每个Sample需要展示01(1,2)--06(1,2)共12个图表，其中.txt文件是每个图表中的数值，.png文件是与数值对应的图表。

补充说明：liuhe 2012011300 @2014/11/12
现在mongodb数据库中的内容：
databases:
	MetaTongueProject:(collections)
		projects 该集合保存MetaTongue工程的信息，包括开始日期、工程名、描述信息等
		samples 该集合保存MetaTongue工程中所有实验用例信息
	projectLists:
		projectInfo 该集合保存ProjectList.xls中的信息
