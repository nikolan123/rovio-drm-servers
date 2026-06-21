from flask import Flask, request, Response
import re

app = Flask(__name__)

@app.route('/consumeKey/', methods=['GET'])
@app.route('/drm/consumeKey/', methods=['GET'])
def drmpc():
    response = f"status=1&type={request.args.get('types')}"
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

    return Response(response, content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
