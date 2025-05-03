from rdflib import Graph
import re
import rdflib
import essential as es
import condition as cond
import difflib
import Levenshtein
# get the distinct list
class Context (object):
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
        while es.Version.get_version(self).lower() in s_list:
            s_list.remove(es.Version.get_version(self).lower())
        distinct_s_list = set(s_list)
        return distinct_s_list


    #判别与LMU组合后的period/stage是否包含两个阶段，并进行值的叠加
    def calculate_the_value(LMU,period,stage):
        get=es.Version.combined_word(LMU,period,stage)
        # version=cond.Judgment.condition_of_notgiven()
        if len(get)==2:
                es.Version.add_value(get)

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
        cpatial=Context.detect_captial_letter(version_value)
        if cpatial is True:
            label_captial=str(label).capitalize()
        else:
            label_captial = str(label)
        if version_value is not None:
            if str(label_captial).lower() in Context.get_distinct_label(version_value):
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







