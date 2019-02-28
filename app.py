from flask import Flask
from flask import request, Response, send_from_directory, jsonify, make_response,render_template
from werkzeug.routing import BaseConverter
from crawlertask import *
from urllib.parse import quote_plus
from confs.conf import *
import json
import redis

app = Flask(__name__,template_folder='report',static_folder="report",static_url_path="")

class RegexConverter(BaseConverter):
    def __init__(self, url, *args):
        self.url = url
        self.regex = args[0]
app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def hello_world():
    render_template("report.html")

# @app.route('/report/<regex("report\.*\.html"):html>/assets/<string:name>')
@app.route('/report/<string:html>/assets/<string:name>')
def render_css(html,name):
    print("html:"+html)
    return app.send_static_file("assets/"+name)

@app.route('/report/<string:name>/')
def render_report(name):
    print("name:"+name)
    return app.send_static_file(name)
    # return render_template(name)

@app.route('/getReportUrl')
def getReportUrl():
    pass

@app.route("/getmenulist")
def menuReportFilelist():
    # filelist = getmenulist()
    filelist = {}
    downloadlist = {}
    downloadlist['filelist'] = filelist
    response = make_response(jsonify(downloadlist))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/runtask_keywords")
def runtask():
    keywords = request.form['keywords']
    print(keywords)

@app.route("/getTaskStatus",methods=['POST'])
def get_task_status():
    taskid = request.form['taskid']
    redis_cli = redis.StrictRedis(host=redis_host,port=redis_port,db=0)
    return jsonify(redis_cli.get(redis_result_prefix+taskid))


@app.route("/download", methods=['POST'])
def downloadreport():
    filename = request.form["filename"]
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    response = make_response(send_from_directory(dirname, basename, as_attachment=True))
    response.headers["Content-Disposition"] += "attachment; filename*=UTF-8''{}".format(
        quote_plus(basename.encode('utf-8')))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/runtask", methods=['GET','POST'])
def getReport():
    """
    platform:
    :return:
    """

    print("get")
    print("**********************************************************************")
    print(request.headers)
    print(request.form['type'])
    print(request.form['keywords'])

    print("**********************************************************************")
    # if str(request.form['type']) == "keyword":
    result = run_task.apply_async(kwargs={"type": request.form['type'],
                                  "keywords": request.form.getlist('keywords')
                                 })

    # "platform": 1  # 1 代表饿了么，2代表美团，3代表全部
    # res = Response("success,waiting...")
    res = make_response(json.dumps({"status":result.status,"id":result.id}))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

