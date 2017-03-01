# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import api

def read_index():
    problem_list = []
    f = open("./raw_txt/index.txt")
    lines = f.readlines()
    f.close()
    father = 0
    for line in lines:
        line = line.strip().replace('(', "（")
        line = line.strip().replace(')', "）")
        line = line.replace("　", "")
        if line == "":
            continue
        index = 1
        level = 2
        if line.strip().find("一、") == 0:
            index = 1
            level = 1
        if line.strip().find("二、") == 0:
            index = 2
            level = 1
        if line.strip().find("三、") == 0:
            index = 3
            level = 1
        if line.strip().find("四、") == 0:
            index = 4
            level = 1
        if line.strip().find("五、") == 0:
            index = 5
            level = 1
        if line.strip().find("六、") == 0:
            index = 6
            level = 1
        if line.strip().find("七、") == 0:
            index = 7
            level = 1
        if line.strip().find("八、") == 0:
            index = 8
            level = 1
        if line.strip().find("九、") == 0:
            index = 9
            level = 1
        if line.strip().find("1、") != -1:
            index = 1
        if line.strip().find("2、") != -1:
            index = 2
        if line.strip().find("3、") != -1:
            index = 3
        if line.strip().find("4、") != -1:
            index = 4
        if line.strip().find("5、") != -1:
            index = 5
        if line.strip().find("6、") != -1:
            index = 6
        if line.strip().find("7、") != -1:
            index = 7
        if line.strip().find("8、") != -1:
            index = 8
        if line.strip().find("9、") != -1:
            index = 9
        if len(line.split('、')) < 2:
            continue
        problem = line.strip().split('、')[1]
        problem_info = {}
        problem_info["problem"] = problem.strip()
        problem_info["level"] = level
        problem_info["index"] = index
        if level == 1:
            father = index
        problem_info["father"] = father
        print problem_info["problem"], problem_info["level"], problem_info["index"], problem_info["father"]
        api.db_api.add(problem_info)

if __name__ == '__main__':
    read_index()
