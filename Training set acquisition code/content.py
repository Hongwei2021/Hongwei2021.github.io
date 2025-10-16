from rdflib import Graph
import re
import rdflib
import essential as es
import condition as cond
import difflib
import Levenshtein
# get the distinct list
class Context (object):
    # Obtain the unique names of periods/stages in the version
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


    #Obtain the determination of whether the period/stage after combining with LMU includes two stages, and perform the value addition.
    def calculate_the_value(LMU,period,stage):
        get=es.Version.combined_word(LMU,period,stage)
        # version=cond.Judgment.condition_of_notgiven()
        if len(get)==2:
                es.Version.add_value(get)

    # Adjust the "period/stage" in the TTL to match the case (uppercase/lowercase) of the original data.
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

    #Obtain the starting boundary value and the uncertain value of the period/stage
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








