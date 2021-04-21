# -*- coding: UTF-8 -*-
# zhutj 2019/3/10
import sys,shutil

#-------以workspace为相对路径，定义要复制文件源、目的路路径------
#注意斜杠统一使用"/""
copyFiles=[
["/oit-v1.0/oit-parent-with-dependencies/TestConfig/common.js","/oit-v1.0/oit-parent-with-dependencies/oit-pcweb/src/main/webapp/web/js/common.js"],
]


#-----------------------------end------------------------------

workspacePath=sys.argv[1]  

for m_file in copyFiles:
	shutil.copyfile(workspacePath+m_file[0],workspacePath+m_file[1])

