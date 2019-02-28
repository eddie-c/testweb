from celery import Celery
import celery
import sys,os
import time
import datetime
from bs4 import BeautifulSoup

sys.path.append(os.getcwd()+"/../")
# 消息类型
app = Celery('tasks', broker='redis://127.0.0.1:7000',backend='redis://127.0.0.1:7001')

app.conf.update(
    CELERY_ACKS_LATE=True,
    CELERY_ACCEPT_CONTENT=['pickle', 'json'],
    CELERYD_FORCE_EXECV=True,
    CELERYD_MAX_TASKS_PER_CHILD=500,
    BROKER_HEARTBEAT=0,
)

@celery.task(bind=True)
def run_task(self,**msgdict):
    run_type = msgdict['type']
    if run_type == "keyword":
        keywordlist = msgdict['keywords']
        timestr = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M%S")
        teststr = run_type + "_" + "_".join(keywordlist)
        print(keywordlist)
        keystr = " or ".join(keywordlist)
        outfile = "report_"+ teststr + timestr +".html"
        outfile_path = "report/" + outfile
        cmd = "pytest /home/eddie/PycharmProjects/testweb/interfaces -k \"" + keystr + "\" --html="+outfile_path
        res = os.popen(cmd,'w')
        print(os.getcwd())
        print("outfile_path:"+outfile_path)
        # time.sleep(10)
        while not os.path.exists(outfile_path):
            time.sleep(1)
        print("file exists:",os.path.exists(outfile_path))
        print(open(outfile_path).read())
        html = BeautifulSoup(open(outfile_path,"r").read())

        passed = int(html.find(class_="passed").text.split(" ")[0])
        failed = int(html.find(class_="failed").text.split(" ")[0])
        print(res)
        if (passed > 0 and failed == 0):
            status = 'success'
        elif failed > 0:
            status = 'failed'
        elif passed == 0 and failed == 0:
            status = 'norun'
        else:
            status = "undefined"

        resdata = {
            "report":outfile,
            "passed":passed,
            "failed":failed,
            #如果错误数>0,返回fail，否则返回success
            "status": status
        }

        return resdata

    elif run_type == "category":
        categories = msgdict['categories']
        print(categories)
    else:
        print("???")


def test_add():
    pass


if __name__=="__main__":
    app.start()
