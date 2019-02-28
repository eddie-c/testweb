import requests
import json
import time

def test_runtask_keyword():
    url = "http://127.0.0.1:5000/runtask"
    data = {
        'type':'keyword',
        'keywords':['add','sub']
    }
    res = requests.post(url,data=data)
    print(res.content)
    return json.loads(res.content.decode("utf-8"))

def test_get_report(html):
    url = "http://127.0.0.1:5000/report/"+html
    res = requests.get(url)
    print(res.content)

def test_get_status(taskid):
    url = "http://127.0.0.1:5000/getTaskStatus"
    data = {
        "taskid":taskid,
    }
    res = requests.post(url,data=data)
    # print(res.content.decode("utf-8"))
    # print(json.loads(res.content.decode("utf-8")))
    jsonobj = json.loads(res.content.decode("utf-8"))
    # print("raw type:",type(jsonobj))
    if jsonobj is None:
        jsonobj = {"status": "PENDING", "id": taskid}
        return jsonobj
    else:
        print(res.content.decode("utf-8"))
        print(json.loads(res.content.decode("utf-8")))
        jsonobj = json.loads(json.loads(res.content.decode("utf-8")))
        return jsonobj

if __name__=="__main__":
    jsonobj = test_runtask_keyword()
    taskid = jsonobj['id']
    # test_get_report()
    res = test_get_status(taskid)
    while res['status'] == "PENDING":
        time.sleep(1)
        res = test_get_status(taskid)
        print("type:",type(res))