import firebase_admin
from firebase_admin import credentials
from firebase_admin.auth import verify_id_token, RevokedIdTokenError, ExpiredIdTokenError, InvalidIdTokenError, CertificateFetchError

from app.core.config import get_settings


_firebase_app: firebase_admin.App | None = None
_firebase_initialized: bool = False


def init_firebase() -> firebase_admin.App | None:
    global _firebase_app, _firebase_initialized
    if _firebase_initialized:
        return _firebase_app

    settings = get_settings()

    if not settings.is_firebase_configured():
        if settings.ENVIRONMENT == "development":
            _firebase_initialized = True
            return None
        raise RuntimeError(
            "Firebase no está configurado. Verifica las variables de entorno FIREBASE_*"
        )

    cred = credentials.Certificate(settings.firebase_credentials_dict)
    _firebase_app = firebase_admin.initialize_app(cred, {
        "projectId": settings.FIREBASE_PROJECT_ID,
    })
    _firebase_initialized = True
    return _firebase_app


def get_firebase_app() -> firebase_admin.App | None:
    if not _firebase_initialized:
        return init_firebase()
    return _firebase_app


async def verify_firebase_token(id_token: str) -> dict:
    app = get_firebase_app()
    if app is None:
        raise ValueError("Firebase no está configurado")
    try:
        decoded_token = verify_id_token(id_token, app=app)
        return decoded_token
    except ExpiredIdTokenError:
        raise ValueError("Token expirado")
    except RevokedIdTokenError:
        raise ValueError("Token revocado")
    except InvalidIdTokenError:
        raise ValueError("Token inválido")
    except CertificateFetchError:
        raise ValueError("Error al obtener certificados de Firebase")
    except Exception as e:
        raise ValueError(f"Error verificando token: {str(e)}")


def verify_firebase_token_sync(id_token: str) -> dict:
    app = get_firebase_app()
    if app is None:
        raise ValueError("Firebase no está configurado")
    try:
        return verify_id_token(id_token, app=app)
    except ExpiredIdTokenError:
        raise ValueError("Token expirado")
    except RevokedIdTokenError:
        raise ValueError("Token revocado")
    except InvalidIdTokenError:
        raise ValueError("Token inválido")
    except CertificateFetchError:
        raise ValueError("Error al obtener certificados de Firebase")
    except Exception as e:
        raise ValueError(f"Error verificando token: {str(e)}")