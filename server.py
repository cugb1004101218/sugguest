# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options
import pymongo
import json
import sys
import api

from tornado.options import define, options
define("port", default=2000, help="run on the given port", type=int)
define("ip", default="0.0.0.0", help="server_ip", type=str)

class ProblemHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def get_ret(self):
        try:
            father = int(self.get_argument('father'))
        except:
            father = 0
        try:
            index = int(self.get_argument('index'))
        except:
            index = 0
        query_keyword = self.get_argument('query', "")
        print index
        query = {}
        if father > 0:
            query["father"] = father
        if index > 0:
            query["index"] = index
        if query_keyword == "":
            problem = api.db_api.get_one({"father":father, "level": 1})
            suggestion_list = api.suggestion_db_api.get_all(query)
        else:
            suggestion_list = api.global_fuzzy_search(query_keyword)
        ret = []
        for suggestion in suggestion_list:
            ret.append([suggestion["name"],suggestion["title"], suggestion["content"]])
        if query_keyword != "":
            return {"suggest_list": ret}
        index_str = ""
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
        if index > 0:
            problem["problem"] = ""
        return {"suggest_list": ret, "problem": problem}

    def get(self):
        # 先从 cache 中取
        ret = self.get_ret()
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(ret))
        self.finish()

class IndexHandler(tornado.web.RequestHandler):
    def gen_tree(self):
        problem_list = []
        all_node = api.db_api.get_all({"level": 1})
        for node in all_node:
            node_info = {}
            index = node["index"]
            child_node = api.db_api.get_all({"level": 2, "father": index})
            child_list = []
            for child in child_node:
                child_list.append({"name": str(child["index"]) + ". " + child["problem"], "url":"http://115.28.145.36:7878?father=" + str(index) + "&index=" + str(child["index"])})
            index_str = ""
            if index == 1: index_str = "一"
            if index == 2: index_str = "二"
            if index == 3: index_str = "三"
            if index == 4: index_str = "四"
            if index == 5: index_str = "五"
            if index == 6: index_str = "六"
            if index == 7: index_str = "七"
            if index == 8: index_str = "八"
            if index == 9: index_str = "九"
            node_info["name"] = "关注之"  + index_str + "：" + node["problem"]
            node_info["children"] = child_list
            problem_list.append(node_info)
        return {"node": problem_list}

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def get(self):
        # 先从 cache 中取
        ret = self.gen_tree()
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(ret))
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/index", IndexHandler), (r"/problem", ProblemHandler)])
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port, address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
