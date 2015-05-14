import hashlib
import time
from lxml import etree
from flask import Flask, request, render_template

TOKEN = 'weixin'
app = Flask(__name__)


def check_signature(token):
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    try:
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        hash_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        if hash_str == signature:
            return True
        else:
            return False
    except TypeError as e:
        print(str(e))
        return False


def post():
    str_xml = request.data
    xml = etree.fromstring(str_xml)
    content = xml.find("Content").text + " handled by python."
    msg_type = xml.find("MsgType").text
    to_user = xml.find("FromUserName").text
    from_user = xml.find("ToUserName").text
    view_obj = {'content': content,
                'msg_type': msg_type,
                'from_user': from_user,
                'to_user': to_user,
                'create_time': int(time.time())
                }
    return render_template("reply_text.xml", view_obj=view_obj)


@app.route('/', methods=['GET', 'POST'])
def index():
    echo_str = request.args.get("echostr")
    # echostr校验
    if echo_str is not None:
        if check_signature(TOKEN):
            return echo_str
        else:
            return 'ok'
    # 消息处理
    else:
        return post()


if __name__ == '__main__':
    app.run(debug=True)