from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback
from authx.exceptions import MissingCSRFTokenError, MissingTokenError


class AuthExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not self._should_handle(request):
            return await call_next(request)
        try:
            return await call_next(request)
        except (MissingTokenError, MissingCSRFTokenError) as exc:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing refresh token"}
            )
    def _should_handle(self, request: Request) -> bool:
        path_to_handle = "/auth"
        return request.url.path.startswith(path_to_handle)