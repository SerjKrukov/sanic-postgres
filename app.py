from sanic import Sanic
from sanic.response import json
from blueprint import bp

app = Sanic(__name__)
app.blueprint(bp)
app.run(host='0.0.0.0.', port=8000, debug=True)
