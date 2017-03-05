# -*- coding: utf-8 -*-
import pymongo
import redis
import sys
import re
import configure
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

class RedisAPI(object):
    def __init__(self, redis_ip, redis_port, redis_db):
        self.conn = redis.Redis(host=redis_ip, port=redis_port, db=redis_db)

    def set(self, k, v, ttl=None):
        ret = self.conn.set(k, v)
        if ttl:
            ret &= self.conn.expire(k, ttl)
        return ret

    def get(self, k):
        return self.conn.get(k)

    def delete(self, k):
        return self.conn.delete(k)

redis_api = RedisAPI(configure.redis_ip, configure.redis_port, configure.redis_db)

class DBAPI(object):
    def __init__(self, db_ip, db_port, db_name, table_name):
        self.db_ip = db_ip
        self.db_port = db_port
        self.db_name = db_name
        self.table_name = table_name
        self.conn = pymongo.MongoClient(host=self.db_ip, port=self.db_port)
        self.db = self.conn[self.db_name]
        self.table = self.db[self.table_name]

    def get_one(self, query):
        return self.table.find_one(query, projection={"_id": False})

    def get_all(self, query):
        return self.table.find(query)

    def add(self, kv_dict):
        return self.table.insert(kv_dict)

    def delete(self, query):
        return self.table.delete_many(query)

    def check_exist(self, query):
        ret = self.get(query)
        return len(ret) > 0

    # 如果没有 会新建
    def update(self, query, kv_dict):
        ret = self.table.update_many(
            query,
            {
                "$set": kv_dict,
            }
        )
        if not ret.matched_count or ret.matched_count == 0:
            self.add(kv_dict)
        elif ret.matched_count and ret.matched_count > 1:
            self.delete(query)
            self.add(kv_dict)

# 资讯数据库API
db_api = DBAPI(configure.db_ip,
               configure.db_port,
               configure.db_name,
               configure.problem_table_name)

suggestion_db_api = DBAPI(configure.db_ip,
                          configure.db_port,
                          configure.db_name,
                          configure.suggestion_table_name)

def global_fuzzy_search(query):
    pattern = re.compile(".*" + query + ".*")
    return suggestion_db_api.get_all({"$or": [{"team": pattern}, {"content": pattern}, {"name": pattern}, {"title": pattern}]})

def get_problem(father, index):
    problem = {"problem":{"problem": ""}}
    mongo_query = {}
    if father.isdigit():
        mongo_query["father"] = int(father)
        mongo_query["level"] = 1
    if index.isdigit():
        mongo_query["index"] = int(index)
        mongo_query["level"] = 2
    problem = db_api.get_one(mongo_query)
    return gen_real_problem(problem)

def gen_real_problem(problem):
    if problem["level"] == 1:
        index_str = ""
        father = problem["father"]
        if father == 1: index_str = "一"
        if father == 2: index_str = "二"
        if father== 3: index_str = "三"
        if father == 4: index_str = "四"
        if father == 5: index_str = "五"
        if father == 6: index_str = "六"
        if father == 7: index_str = "七"
        if father == 8: index_str = "八"
        if father == 9: index_str = "九"
        problem["problem"] = "关注之" + index_str + "：" + problem["problem"]
    elif problem["level"] == 2:
        problem["problem"] = str(problem["index"]) + ". "  + problem["problem"]
    return problem

if __name__ == '__main__':
    #problem = {"title":"服务改革和经济社会发展大局"}
    #db_api.add(problem)
    #print db_api.get_one({"title":"服务改革和经济社会发展大局"})
    for i in global_fuzzy_search("军队"):
        print i
