from sanic import Blueprint
from sanic.response import json

bp = Blueprint(url_prefix='api', name='my_blueprint')

@bp.get('/user')
async def getAll(request):
    return json({'status':'all'})

@bp.post('/user')
async def create(request):
    return json({'status':'post'})

@bp.patch('/user/<id:int>')
async def update(request, id):
    return json({'update': id})

@bp.delete('/user/<id:int>')
async def delete(request, id):
    return json({'delete': id})
