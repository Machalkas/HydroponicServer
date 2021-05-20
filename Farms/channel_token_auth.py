from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from .models import Farm
from Users.models import User


@database_sync_to_async
def getUserFromToken(key):
    t=Token.objects.get(key=key)
    return User.objects.get(pk=t.user.pk)
@database_sync_to_async
def getFarmToken(key):
    try:
        return Farm.objects.get(token=key)
    except:
        return None

class TokenAuthMiddleware:

    def __init__(self, app):
        self.app=app

    async def __call__(self, scope, receive, send):
        query=dict(x.split("=") for x  in scope["query_string"].decode().split("&"))
        try:
            token_name, token_key=query['Authorization'].split("%20")
            if token_name=="Token":
                scope['is_farm']=False
                user= await getUserFromToken(token_key)
                scope['user']=user
            elif token_name=="FarmToken":
                scope['is_farm']=True
                farm=await getFarmToken(token_key)
                scope['farm']=farm
        except Token.DoesNotExist:
            scope['user']=AnonymousUser()
        return await self.app(scope, receive, send)



TokenAuthMiddlewareStack = lambda app: TokenAuthMiddleware(AuthMiddlewareStack(app))