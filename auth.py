import jwt

from config import BETTER_AUTH_SECRET

def verify_token(token : str):
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        return payload
    
    except Exception:
        return None
    
