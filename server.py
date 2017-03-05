# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import pymongo
import json
import sys
import api
import configure

from tornado.options import define, options
define("port", default=2000, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def gen_cache_key(self):
        return None

    def get_from_cache(self, key):
        if not key:
            return None
        return api.redis_api.get(key)

    def get_from_db(self):
        return None

    def get(self):
        # 先从 cache 中取
        key = self.gen_cache_key();
        result = self.get_from_cache(key)
        if not result:
            print "get from db"
            ret = self.get_from_db()
            result = json.dumps(ret)
            api.redis_api.set(key, result, 3600)
        self.write(result)
        self.finish()

class ProblemHandler(BaseHandler):
    def gen_cache_key(self):
        father = self.get_argument("father", "")
        index = self.get_argument("index", "")
        query = self.get_argument("query", "")
        key = "PROBLEM_HANDLER_" + father + "_" + index + "_" + query
        return key

    def get_suggest_list(self, father, index, query):
        mongo_query = {}
        if father.isdigit():
            mongo_query["father"] = int(father)
        if index.isdigit():
            mongo_query["index"] = int(index)
        ret = []
        if len(query) > 0:  # 全局模糊搜索
            suggestion_list = api.global_fuzzy_search(query).sort("sid")
        else:  # 某个问题下的建议
            suggestion_list = api.suggestion_db_api.get_all(mongo_query).sort("sid")
        for suggestion in suggestion_list:
            ret.append([suggestion["name"], suggestion["team"], suggestion["title"], suggestion["content"]])
        return ret

    def get_problem(self, father, index, query):
        problem = {"problem":{"problem": ""}}
        if len(query) == 0:  # 某个问题
            problem = api.get_problem(father, index)
        else:
            problem = {"problem": "关键字：" + query}
        return problem

    def get_from_db(self):
        father = self.get_argument("father", "")
        index = self.get_argument("index", "")
        query = self.get_argument("query", "")
        suggestion_list = self.get_suggest_list(father, index, query)
        problem = self.get_problem(father, index, query)
        return {"suggest_list": suggestion_list, "problem": problem}

class IndexHandler(BaseHandler):
    def gen_cache_key(self):
        return "INDEX_HANDLER_GET_TREE"
    def gen_tree(self):
        problem_list = []
        all_node = api.db_api.get_all({"level": 1}).sort("index")
        for node in all_node:
            node_info = {}
            index = node["index"]
            child_node = api.db_api.get_all({"level": 2, "father": index}).sort("index")
            child_list = []
            for child in child_node:
                child_list.append({
                    "name": str(child["index"]) + ". " + child["problem"],
                    "url": configure.suggestion_list_page_url + "?father=" + str(index) + "&index=" + str(child["index"])
                })

            node_info["name"] = api.gen_real_problem(node)["problem"]
            node_info["children"] = child_list
            problem_list.append(node_info)
        return {"node": problem_list}

    def get_from_db(self):
        return self.gen_tree()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/index", IndexHandler), (r"/problem", ProblemHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
