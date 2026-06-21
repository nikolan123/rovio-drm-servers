from flask import Flask, request, Response
import logging
import re
from hostsedit import *

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
app.logger.disabled = True
log.disabled = True

def log_request(response):
    print(
        f"Got new request from {request.remote_addr}!\n"
        f"GET {request.base_url}\n"
        f"Key: {request.args.get('key')}\n"
        f"Types: {request.args.get('types')}\n"
        f"UDID: {request.args.get('udid') or request.args.get('uid')}\n"
        f"Returning {response}, 200"
    )


@app.route('/consumeKey/', methods=['GET'])
@app.route('/drm/consumeKey/', methods=['GET'])
def drmpc():
    response = f"status=1&type={request.args.get('types')}"
    log_request(response)
    return Response(response, content_type='text/plain')

CHECK_KEY_REWARDS = {
    "RVMS2013AC": {
        "SUPERSEEDXX": ("RVMS2013AC", "rovio-ad-codes-2"),
    },
    "HSBR2012TS": {
        "BONUSLEVELX": ("HSBR2012", "bonus"),
        "PATHOFJEDIX": ("HSBR2012", "dagobah"),
        "ONEFALCONXX": ("HSBR2012", "falcon"),
        "BOBAFETTXXX": ("HSBR2012", "bobafett"),
    },
    "HSBR2013TS": {
        "CREDITTIERA": ("HSBR2013TS", "cred-tier1"),
        "HASBROCODEA": ("HSBR2013TS", "hasbro-toy-codes-10"),
        "CREDITTIERB": ("HSBR2013TS", "cred-tier2"),
        "HASBROCODEB": ("HSBR2013TS", "hasbro-toy-codes-11"),
    },
}

@app.route('/checkKey/', methods=['GET'])
@app.route('/drm/checkKey/', methods=['GET'])
def check_key():
    key = (request.args.get('key') or '').upper()
    key_type = request.args.get('types') or ''

    if not re.fullmatch(r'[A-Z]{11}', key):
        response = "status=0&msg=invalid-key"
    else:
        reward = CHECK_KEY_REWARDS.get(key_type, {}).get(key)
        if reward is None:
            response = "status=0&msg=invalid-key"
        else:
            response_type, group = reward
            response = f"status=1&type={response_type}&group={group}"

    log_request(response)
    return Response(response, content_type='text/plain')

if __name__ == '__main__':
    confirm = input("Would you like the script to modify your hosts file to redirect Rovio servers to 127.0.0.1? (y/n): ").lower()
    if confirm == 'y':
        print(addrovio("127.0.0.1"))
    else:
        print("Will not touch the hosts file.")

    app.run(debug=False, host="127.0.0.1", port=80)
