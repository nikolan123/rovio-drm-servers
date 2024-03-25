from flask import Flask, request, Response
import logging
from hostsedit import *

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
app.logger.disabled = True
log.disabled = True
    
@app.route('/consumeKey/', methods=['GET'])
@app.route('/drm/consumeKey/', methods=['GET'])
def drmpc():
    response = f"status=1&type={request.args.get('types')}"
    print(f"Got new request from {request.remote_addr}!\nGET {request.base_url}\nKey: {request.args.get('key')}\nTypes: {request.args.get('types')}\nUDID: {request.args.get('udid')}\nReturning {response}, 200")
    return Response(response, content_type='text/plain')

if __name__ == '__main__':
    print(addrovio("127.0.0.1"))
    app.run(debug=False, host="127.0.0.1", port=80)
