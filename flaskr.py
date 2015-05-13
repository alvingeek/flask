import hashlib
from flask import Flask, request

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
    finally:
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    echo_str = request.args.get("echostr")
    if echo_str is not None:
        if check_signature(TOKEN):
            return echo_str
        else:
            return 'ok'
    else:
        return ''


if __name__ == '__main__':
    app.run(debug=True)