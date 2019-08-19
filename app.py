from sanic import Sanic
from sanic.response import json
from sanic.exceptions import abort
from blueprint import bp
from gino.ext.sanic import Gino

app = Sanic()
app.config.DB_HOST = 'ec2-54-228-243-238.eu-west-1.compute.amazonaws.com'
app.config.DB_DATABASE = 'd5vbjksh0aovib'
app.config.DB_USER = 'cptwarcybkjxed'
app.config.DB_PASSWORD = '84f2039c559006c9165f9aea1cc4d4766f85be6e9e51362243fa157a44c1692c'
app.config.DB_SSL = 'require'
db = Gino()
db.init_app(app)
app.blueprint(bp)


class User(db.Model):
    __tablename__ = 'modelusers'

    id = db.Column(db.BigInteger(), primary_key=True)
    nickname = db.Column(db.Unicode())

    def __repr__(self):
        return '{}<{}>'.format(self.nickname, self.id)

@app.post('/users')
async def create_user(request):
    user = await User.create(nickname='fantix')

@app.route("/users/<user_id>")
async def get_user(request, user_id):
    if not user_id.isdigit():
        abort(400, 'invalid user id')
    user = await User.get_or_404(int(user_id))
    return json({'name': user.nickname})


if __name__ == '__main__':
    app.run(host='0.0.0.0.', port=9000, debug=True)