import jwt

from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires authentication",
        )


class VerifyToken:
    def __init__(self, settings):
        self.settings = settings
        jwks_url = f"https://{self.settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def with_scopes(self, *scopes: str):
        self.scopes = scopes
        return self

    async def verify(
        self,
        token: str,
    ):
        if token is None:
            raise UnauthenticatedException

        try:
            payload = jwt.decode(
                token.credentials,
                self.settings.SECRET_KEY,
                algorithms=self.settings.AUTH0_ALGORITHM,
                audience=self.settings.AUTH0_AUDIENCE,
                issuer=self.settings.AUTH0_ISSUER,
            )

            if not all(scope in payload.get("scope", "") for scope in self.scopes):
                raise UnauthorizedException("Insufficient scope")

        except Exception as error:
            raise UnauthorizedException(str(error))

        return payload
