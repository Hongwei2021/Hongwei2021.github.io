from rdflib import Graph
import rdflib
import content as con
import pandas
import re
import csv
from sklearn import preprocessing, tree
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier


#将原始数据中的LMU进行全称的替换与校正
def search_label(LUM):
    value = re.findall(r'[A-Z]', LUM)
    if len(value) >= 2:
        if value == ["L", "M"]:
            return "early", "middle"
        if value == ["M", "U"]:
            return "middle", "late"
        if value == ["L", "U"]:
            return "early", "late"
        if value == ["M", "L"]:
            return "middle", "early"
        if value == ["L", "M", "U"]:
            return None
    else:
        if value == ["L"]:
            return "early"
        if value == ["M"]:
            return "middle"
        if value == ["U"]:
            return "late"



# 对于包含有两个阶段（例如middle——permain，late——permian）的period/stage，进行数值的叠加计算
def add_value(version, self):
    end = {}
    start = {}
    end_uncertainty = {}
    start_uncertainty = {}
    for item in self:
        get = con.Context.get_boundary_value(version, item)
        end[item] = get[0]
        start[item] = get[2]
        end_uncertainty[item] = get[1]
        start_uncertainty[item] = get[3]
    final_end = end[self[1]]
    final_start = start[self[0]]
    final_end_uncertainty = end_uncertainty[self[1]]
    final_start_uncertainty = start_uncertainty[self[0]]
    print(final_end, final_start, final_end_uncertainty, final_start_uncertainty)
    return final_end, final_end_uncertainty, final_start, final_start_uncertainty



#将LMU与period/stage进行组合
def combined_word(LUM ,period ,stage):
    label_list = []
    if stage is not None  :  # 如果有stage，对stage进行判别
        if period is None and LUM is not None:
            lum = search_label(LUM)
            if lum == None:
                label = stage
                return label.lower()
            else:
                if len(lum) == 2:
                    for item in lum:
                        label = item + '_' + stage
                        label_list.append(label.lower())
                    return label_list
                if len(lum) != 2:
                    label = lum + '_' + stage
                    return label.lower()
        if period is not None:
            label =stage
            return label.lower()
        if LUM is None:
            label = stage
            return label.lower()
    if stage is None  :  # 如果没有stage，对period进行判别
        if period is not None and LUM is not None:
            lum = search_label(LUM)
            if lum == None:
                label = period
                return label.lower()
            else:
                if len(lum) == 2:
                    for item in lum:
                        label = item + '_' + period
                        label_list.append(label.lower())
                    return label_list
                if len(lum) != 2:
                    label = lum + '_' + period
                    return label.lower()

        if LUM is None and period is not None:
            label =period
            return label.lower()
        if LUM is None and period is None:
            print("no enough information")
            return None

# 获得地质年代版本
def get_version(self):  #self is the file path
    graph = Graph()
    graph_path = 'H:/test/' + (str(self) + '.ttl')
    graph.parse(graph_path, format='ttl')
    version_URL = graph.value(predicate=rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                              object=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#reference_system'),
                              any=False)
    # print(version_URL)
    version_URL_string = str(version_URL)
    searchObj = re.search(r'utf#(.*)', version_URL_string, re.M | re.I)
    version_value = searchObj.group(1)
    #print(version_value)
    return version_value



# 获得版本中不重复的period/stage名称
def get_distinct_label(self):
    s_list = []
    graph = Graph()
    graph_path = 'H:/test/' + (str(self)) + '.ttl'
    graph.parse(graph_path, format='ttl')
    for s, p, o in graph:
        s_string = str(s)
        searchObj = re.search(r'utf#(.*)', s_string, re.M | re.I)
        s_value = searchObj.group(1)
        s_value_low=s_value.lower()
        s_list.append(s_value_low)
    while get_version(self).lower() in s_list:
        s_list.remove(get_version(self).lower())
    distinct_s_list = set(s_list)
    return distinct_s_list




# 适配ttl中的period/stage与原始数据中的大小写
def detect_captial_letter(self):
    s_list = []
    graph = Graph()
    graph_path = 'H:/test/' + (str(self)) + '.ttl'
    graph.parse(graph_path, format='ttl')
    for s, p, o in graph:
        s_string = str(s)
        searchObj = re.search(r'utf#(.*)', s_string, re.M | re.I)
        s_value = searchObj.group(1)
        s_list.append(s_value)
    if s_list[0].islower() is True:
        return False
    else:
        return True






#获取period/stage的起始边界值和边界值不确定值
def get_boundary_value(version_value,label):
    #version_value=es.Version.get_version(self)
    graph = Graph()
    graph_path='H:/test/'+(str(version_value))+'.ttl'
    graph.parse(graph_path, format='ttl')
    cpatial=detect_captial_letter(version_value)
    if cpatial is True:
        label_captial=str(label).capitalize()
    else:
        label_captial = str(label)
    if version_value is not None:
        if str(label_captial).lower() in get_distinct_label(version_value):
                start_value = graph.value(
                    subject=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#' + str(label_captial)),
                    predicate=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#start'),
                    any=False)
                end_value = graph.value(
                    subject=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#' + str(label_captial)),
                    predicate=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#end'),
                    any=False)
                start_uncertainty_value = graph.value(
                    subject=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#' + str(label_captial)),
                    predicate=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#start_uncertainty'),
                    any=False)
                end_uncertainty_value = graph.value(
                    subject=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#' + str(label_captial)),
                    predicate=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#end_uncertainty'),
                    any=False)
                print("the converted geological time scale is :%s±%s - %s±%s Ma" %(str(end_value),str(end_uncertainty_value),str(start_value),str(start_uncertainty_value)))
                return start_value, start_uncertainty_value,end_value, end_uncertainty_value
        else:
                print("not in the list")
                start_value = None
                end_value = None
                start_uncertainty_value = None
                end_uncertainty_value = None
                return start_value, start_uncertainty_value, end_value, end_uncertainty_value
    else: return None

#读取原始数据，ttl数据库，并写入输出文件中
def out(rawdata,output,ttlpath):
    data= pandas.read_excel(rawdata,engine='openpyxl',sheet_name="Sheet1")
    df = data.where(data.notnull(), None)
    with open(output,'w',encoding='utf-8',newline='') as targetFile:  #with putting "newlinw=''"into the open , there will be no space between each line
        for m in range(0,2479): #0-139
            print(m)
            file=ttlpath
            LMU=df.iat[m,0]
            period=df.iat[m,1]
            stage=df.iat[m,2]
            version=df.iat[m,3]
            label=combined_word(LMU,period,stage)
            result=get_boundary_value(version,label)
            if result is not None:
                writer = csv.writer(targetFile)
                writer.writerow((result[0],result[1], result[2], result[3],version))
                print("successful")
            else:
                writer = csv.writer(targetFile)
                writer.writerow((None, None, None, None))
                print("successful")
                continue
#数据库预处理，把训练集和竞赛数据集里的字符串特征转换成数字
def convert_to_category(data,comp_data):
    labelencoder = preprocessing.LabelEncoder()
    code_feat = pd.DataFrame()
    comp_code_feat = pd.DataFrame()
    train_feat = data
    code_set = {}
    for f in train_feat:
        name = f
        if f not in ['LithologyIDNumber','LAT','LONG','Year','OldIDNumber','Start','End','Start_uncertainty','End_uncertainty','Version']:
            labelencoder = preprocessing.LabelEncoder()
            f_code = labelencoder.fit(train_feat[f])
            comp_f = f_code.transform(comp_data[f])
            f = labelencoder.fit_transform(train_feat[f])
            f = pd.Series(f, dtype="category")
            code_set[name] = f_code.classes_
            if not isinstance(f_code.classes_[-1],str):
                a = f_code.classes_
                map = {len(a)-1:a[-1]}
                f = f.replace(map)
                b = dict(zip(np.arange(0,len(a),1),a))
                code_set[name]=b
            code_feat[name] = f
            comp_code_feat[name] = comp_f

            # code_set[name]=b
        else:
            code_feat[name] = train_feat[f]
            comp_code_feat[name] = comp_data[f]
    code_feat = np.array(code_feat)
    code_feat = pd.DataFrame(code_feat, columns=data.columns)

    return code_set, code_feat, comp_code_feat

#基于训练集构建分类模型，对竞赛集进行预测
def ML_method(train_file_name, test_file_name):
    # train_file_name = '训练数据.csv'
    dataset = pd.read_csv(train_file_name)
    # test_file_name = 'test_set.csv'
    test_set = pd.read_csv(test_file_name)
    feat = dataset
    label_version = feat.iloc[:,feat.columns == 'Version']
    label_end = feat.iloc[:,feat.columns != 'End']   
    label_start = feat.iloc[:,feat.columns != 'Start']
    label_suncert = feat.iloc[:,feat.columns != 'Start_uncertainty']
    label_euncert = feat.iloc[:,feat.columns != 'End_uncertainty']
    feat = feat.iloc[:,feat.columns != 'Version']
    feat = feat.iloc[:,feat.columns != 'End']   
    feat = feat.iloc[:,feat.columns != 'Start']
    feat = feat.iloc[:,feat.columns != 'Start_uncertainty']
    feat = feat.iloc[:,feat.columns != 'End_uncertainty']
    feat = feat.iloc[:,feat.columns != 'Version']

    code, feat, test_feat = convert_to_category(feat,test_set)

    imp_mean = KNNImputer(n_neighbors=3, weights="uniform")
    imp_mean.fit(feat)
    complete_feat = imp_mean.transform(feat)
    imp_mean.fit(test_feat)
    complete_test_feat = imp_mean.transform(test_feat)

    clf2 = KNeighborsClassifier(n_neighbors=1)
    model_knn = clf2.fit(complete_feat, label_version)
    p = model_knn.predict(complete_test_feat)
    df = pd.DataFrame(p)
    df.to_csv('res.csv', index = False, header = None)

if __name__ == "__main__":
    out('H:/competition/final/test_2004.xlsx','H:/competition/final/result_test_2004.csv',"H:/competition/database")
    ML_method('训练数据.csv','test_set.csv')
