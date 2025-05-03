from rdflib import Graph
import rdflib
import math
import re
import content as con
class Version(object):
    #获取地质年代版本合集
    def get_version_list(self): #
        s = []
        for file in self:  # 遍历文件夹
            graph = Graph()
            graph.parse(file, format='ttl')
            version_URL = graph.value(predicate=rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                                      object=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#reference_system'),
                                      any=False)
            # print(version_URL)
            version_URL_string = str(version_URL)
            searchObj = re.search(r'utf#(.*)', version_URL_string, re.M | re.I)
            version_value = searchObj.group(1)
            s.append(version_value)  # 每个文件的文本存到list中
            # print(version_value)
        # print(s)
        return s

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

   #将LMU与period/stage进行组合
    def combined_word(LUM,period,stage):
        label_list = []
        if stage is not None:#如果有stage，对stage进行判别
            if period is None and LUM is not None:
                lum = Version.search_label(LUM)
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
                label=stage
                return label.lower()
            if LUM is None:
                label = stage
                return label.lower()
        if stage is None:#如果没有stage，对period进行判别
            if period is not None and LUM is not None:
                lum = Version.search_label(LUM)
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
                label=period
                return label.lower()
            if LUM is None and period is None:
                print("no enough information")
                return None


    #获得包含有目标stage/period的地质年代版本名称
    def detect_version_list(path,LUM,period,stage):
        v_list=[]
        get=Version.combined_word(LUM,period,stage)
        print(get)
        if get is not None:
            if len(get)==2:
                for version in Version.get_version_list(path):  # get the version list
                    for item in get:
                        if item in con.Context.get_distinct_label(version):  # get the labels in each version
                            v_list.append(version)
                return v_list,get
            else:
                for version in Version.get_version_list(path):  # get the version list
                    if get in con.Context.get_distinct_label(version):  # get the labels in each version
                        v_list.append(version)
                return v_list,get
        else: return None

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

    #对于包含有两个阶段（例如middle——permain，late——permian）的period/stage，进行数值的叠加计算
    def add_value(version,self):
            end={}
            start={}
            end_uncertainty = {}
            start_uncertainty = {}
            for item in self:
                get=con.Context.get_boundary_value(version,item)
                end[item]=get[0]
                start[item]=get[2]
                end_uncertainty[item]=get[1]
                start_uncertainty[item]=get[3]
            final_end=end[self[1]]
            final_start=start[self[0]]
            final_end_uncertainty=end_uncertainty[self[1]]
            final_start_uncertainty = start_uncertainty[self[0]]
            print(final_end,final_start,final_end_uncertainty,final_start_uncertainty)
            return final_end,final_end_uncertainty,final_start,final_start_uncertainty
















