from rdflib import Graph
import rdflib
import math
import re
import content as con
class Version(object):
    #Obtain the complete collection of geological age versions
    def get_version_list(self): #
        s = []
        for file in self:  #Traverse the folder
            graph = Graph()
            graph.parse(file, format='ttl')
            version_URL = graph.value(predicate=rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                                      object=rdflib.term.URIRef('https://www.ddeworld.org/ddeKG/base/utf#reference_system'),
                                      any=False)
            # print(version_URL)
            version_URL_string = str(version_URL)
            searchObj = re.search(r'utf#(.*)', version_URL_string, re.M | re.I)
            version_value = searchObj.group(1)
            s.append(version_value)  # Store the text of each file in the list.
            # print(version_value)
        # print(s)
        return s

    # Obtain the geological age version
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

   #Combine LMU with period/stage
    def combined_word(LUM,period,stage):
        label_list = []
        if stage is not None:#If there is a stage, make a judgment on the stage.
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
        if stage is None:#If there is no stage, make a judgment on the period
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


    #Obtain the name of the geological era version that includes the target stage/period
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

    #Replace and correct the full names of the LMUs in the original data
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

    #For periods/stages that consist of two phases (for example, middle - permain, late - permian), perform the calculation of adding up the values.
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

















