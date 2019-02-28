import redis
import datetime
from confs.conf import redis_result_prefix
from bs4 import BeautifulSoup
import os

html = BeautifulSoup(open("report/report_keyword_add_sub20190227_163623.html").read())
print(html)
# res = os.popen("ls","r")
# print(res.read())

# redis_host = "127.0.0.1"
#
# taskid = "fe071980-2890-47f7-932c-68b6d8fdab3c"
#
# redis_cli = redis.StrictRedis(host=redis_host,port=7001,db=0)
#
# res = redis_cli.get(redis_result_prefix + taskid)
# print(res)

# now = datetime.datetime.now()
# print(datetime.datetime.strftime(now,"%Y%m%d_%H%M%S"))