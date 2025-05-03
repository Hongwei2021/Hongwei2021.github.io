# coding=utf-8
import  os,sys
import essential as es
import content as con
import path
import condition as cond
import xlrd
import pandas
import re
import csv


#根据period/stage确定最后所采用的版本，并获取对应的起始值及不确定度
def main (file,LMU,period,stage,reference):
    file_list = path.Direction.get_dic_list(file)
    version_list = es.Version.detect_version_list(file_list,LMU,period,stage)
    print(version_list[0],version_list[1])
    if version_list is not None:
        label = version_list[1]
        print(label)
        version = cond.Judgment.condition_of_notgiven(version_list[0], reference)
        print(version)
        if label is not None and version is not None:
            if len(label) == 2:
                value = es.Version.add_value(version, label)
                return value,version
            else:
                value = con.Context.get_boundary_value(version, label)
                return value,version

        else:None
    else: None

#读取原始数据，ttl数据库，并写入输出文件中
def out(rawdata,output,ttlpath):
    data= pandas.read_excel(rawdata,engine='openpyxl',sheet_name="Sheet1")
    df = data.where(data.notnull(), None)
    with open(output,'w',encoding='utf-8',newline='') as targetFile:  #with putting "newlinw=''"into the open , there will be no space between each line
        for m in range(0,139):
            print(m)
            file=ttlpath
            LMU=df.iat[m,10]
            period=df.iat[m,11]
            stage=df.iat[m,12]
            reference=df.iat[m,17]
            get_2= main (file,LMU,period,stage,reference)
            if get_2 is not None:
                writer = csv.writer(targetFile)
                writer.writerow((get_2[0][0],get_2[0][1],get_2[0][2],get_2[0][3],get_2[1]))
                print("successful")
            else:
                writer = csv.writer(targetFile)
                writer.writerow((None, None, None, None))
                print("successful")
                continue

if __name__ == "__main__":
    out('H:/competition/senlling.xlsx','H:/competition/final/senlling_test_result.csv',"H:/competition/database")