from sanic import Sanic
from sanic.response import json
from sanic import response
from sanic.exceptions import abort
from blueprint import bp
from gino.ext.sanic import Gino
import asyncpg
from gino import GinoConnection


app = Sanic(__name__)
app.config.from_pyfile('./.env')
db = Gino()
db.init_app(app)
app.blueprint(bp)


class User(db.Model):
    __tablename__ = 'usersmodels'

    id = db.Column(db.BigInteger(), primary_key=True)
    data = db.Column(db.JSON())

    def __repr__(self):
        return '{}<{}>'.format(self.data, self.id)

@app.post('/users')
async def create_user(request):
    try:

        user = await User.create(data = request.json)
        return json({'id':user.id})

    except asyncpg.exceptions.UniqueViolationError:

        return json({'status': 'failed', 'reason': 'email already exists'})

    except asyncpg.exceptions.CheckViolationError:

        return json({'status': 'failed', 'reason': 'email not valid'})

@app.get("/users/<user_id>")
async def get_user(request, user_id):

    if not user_id.isdigit():
        abort(400, 'invalid user id')

    user = await User.get_or_404(int(user_id))
    user.data['id'] = user.id

    return json(user.data)

@app.get("/users")
async def get_all_users(request):

    all_users = await User.query.gino.all()
    users_list = []

    for user in all_users:
        user.data['id'] = user.id
        users_list.append(user.data)

    return response.json(users_list)

@app.patch("/users/<user_id>")
async def update_user(request, user_id):
    newdata = request.json
    print(newdata)
    id_s = int(user_id)
    if not user_id.isdigit():
        abort(400, 'invalid user id')

    async with db.transaction() as tx:
        user = await User.get_or_404(int(user_id))

        for key, value in request.json.items():
            user.data[key] = value

        await user.update(data = user.data).apply()

    return json(user.data)

@app.delete("/users/<user_id>")
async def del_user(request, user_id):

    if not user_id.isdigit():
        abort(400, 'invalid user id')

    user = await User.get_or_404(int(user_id))
    await user.delete()

    return json({"id": user_id, "status": "deleted"})
# if __name__ == '__main__':
app.run(host='0.0.0.0', port=9000, debug=True)