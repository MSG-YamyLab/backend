from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from urllib.parse import parse_qs

import asyncio 


UserModel = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user = await asyncio.get_event_loop().run_in_executor(None, lambda: UserModel.objects.get(id=access_token["user_id"]))
                scope["user"] = user
            except Exception:
                scope["user"] =  AnonymousUser()

        return await super().__call__(scope, receive, send)

