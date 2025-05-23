import re
import essential as es
import content as con
class Judgment(object):

    #确定最适配的版本名称
    def condition_of_notgiven(v_list,reference):
        version_dic={}
        gap_list=[]
        if v_list is None:
            return None
        else:
            if len(v_list)==0:
                print("unknown version, not in our database")
                return None
            if len(v_list)>=1:
                pattern = re.compile(r'(\d{4})', re.S)
                reference_year = re.findall(pattern, str(reference))
                if reference_year != []:
                    pattern = re.compile(r'(\d{4})', re.S)
                    for item in v_list:
                        version_year = re.findall(pattern, str(item))
                        gap = (int(reference_year[0]) - int(version_year[0]))

                        if int(gap) >= -2 and int(gap) <= 20: # 参考文献中的年份与版本的年份的差值的阈值在20到-2之间
                            gap_list.append(gap)
                            version_dic[gap] = item
                    print(gap_list)
                    if gap_list:
                        if 0 in (gap_list):
                            return version_dic[0]
                        else:
                            return version_dic[min(gap_list)]
                    else:
                        return None















