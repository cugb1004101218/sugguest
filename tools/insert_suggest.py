# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import api
import re

def get_index(s):
    if s.find("（一）") != -1: return 1
    if s.find("（二）") != -1: return 2
    if s.find("（三）") != -1: return 3
    if s.find("（四）") != -1: return 4
    if s.find("（五）") != -1: return 5
    if s.find("（六）") != -1: return 6
    if s.find("（七）") != -1: return 7
    if s.find("（八）") != -1: return 8
    if s.find("（九）") != -1: return 9
    return False

def get_content(s):
    return s.split('建议：')[1].strip()

def get_people_list(s):
    name_title = []
    people_p = re.compile("(.+)（.*）$")
    people_t = re.compile(".+（(.*?![）])）$")
    people_list = ("）".join(s.strip().split('建议：')[0].split('）')[:-1]) + "）").split("）、")
    for i in range(0, len(people_list)):
        people = people_list[i]
        if i < len(people_list) - 1:
            people += "）"
        print people
        people = people.strip()
        name = people.split('（')[0]
        title = "）".join("（".join(people.split('（')[1:]).split('）')[:-1])
        name_title.append([name.strip(), title.strip()])
    return name_title

def read_suggest(father):
    f = open("./raw_txt/" + str(father) + ".txt")
    lines = f.readlines()
    f.close()
    problem = ""
    index = 1
    for line in lines[1:]:
        line = line.strip().replace('(', '（')
        line = line.strip().replace(')', '）')
        line = line.replace("　", "")
        if len(line.strip()) == 0:
            continue
        if get_index(line):
            index = get_index(line)
            continue
        if len(line.split('建议：')) < 2:
            continue
        for people in get_people_list(line):
            suggest_info = {
                "content": get_content(line),
                "index": index,
                "father": father,
                "name": people[0],
                "title": people[1],
            }
            print father, suggest_info["name"], suggest_info["title"], suggest_info["father"], suggest_info["index"], suggest_info["content"]
            api.suggestion_db_api.update(suggest_info, suggest_info)


if __name__ == '__main__':
    for i in range(1, 10):
        read_suggest(i)
