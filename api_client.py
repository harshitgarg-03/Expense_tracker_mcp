import httpx
from config import API_BASE_URL
from session import session
from schemas.expense import ExpenseCreate


class ExpenseApi:
    def __init__(self, token: str | None = None):
        if token is None:
            token = session.token

        headers = {}
        if token:
            cookie_name = getattr(session, "cookie_name", None) or "session_token"
            headers["Cookie"] = f"{cookie_name}={token}"

        self.client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            timeout=30,
            headers=headers
        )

    async def close(self):
        await self.client.aclose()


# ---------------------->>>>>>  GENERIC METHODS  <<<<---------------------


    async def get(self, path: str):
        res = await self.client.get(path)
        res.raise_for_status()
        return res.json()
    
    async def post(self, path: str, data: dict):
        res = await self.client.post(path, json=data)
        res.raise_for_status()
        return res.json()
    
    async def put(self, path: str, data: dict):
        res = await self.client.put(path, json=data)
        res.raise_for_status()
        return res.json()
    
    async def delete(self, path: str):
        res = await self.client.delete(path)
        res.raise_for_status()
        return res.json()


# ---------------------->>>>>>  AUTH SERVICES <<<<---------------------
 

    async def sign_up_user(
        self,
        name: str,
        email: str,
        password: str
    ):
        res = await self.client.post(
            "auth/sign-up/email",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )
        res.raise_for_status()
        data = res.json()

        # Parse session cookie dynamically
        session_cookie_name = "session_token"
        session_cookie_value = None

        # Try parsing from response cookies
        for name_key, val in res.cookies.items():
            if "session_token" in name_key or "better-auth" in name_key:
                session_cookie_name = name_key
                session_cookie_value = val
                break

        # Fallback to manual header parsing
        if not session_cookie_value:
            cookie_header = res.headers.get("set-cookie", "")
            if cookie_header:
                parts = cookie_header.split(";")[0].split("=", 1)
                if len(parts) == 2:
                    name_key = parts[0].strip()
                    if "session_token" in name_key or "better-auth" in name_key:
                        session_cookie_name = name_key
                        session_cookie_value = parts[1].strip()

        if session_cookie_value:
            session.cookie_name = session_cookie_name
            session.token = session_cookie_value
            session.user = data.get("user")

        return {
            "message": "user signup success..",
            "user": session.user
        }

    async def signin_user(self, email: str, password: str):
        res = await self.client.post(
            "auth/sign-in/email",
            json={
                "email": email,
                "password": password
            }
        )

        if res.status_code != 200:
            return {
                "error": "Invalid credentials"
            }

        data = res.json()
        
        # Parse session cookie dynamically
        session_cookie_name = "session_token"
        session_cookie_value = None

        # Try parsing from response cookies
        for name_key, val in res.cookies.items():
            if "session_token" in name_key or "better-auth" in name_key:
                session_cookie_name = name_key
                session_cookie_value = val
                break

        # Fallback to manual header parsing
        if not session_cookie_value:
            cookie_header = res.headers.get("set-cookie", "")
            if cookie_header:
                parts = cookie_header.split(";")[0].split("=", 1)
                if len(parts) == 2:
                    name_key = parts[0].strip()
                    if "session_token" in name_key or "better-auth" in name_key:
                        session_cookie_name = name_key
                        session_cookie_value = parts[1].strip()

        if session_cookie_value:
            session.cookie_name = session_cookie_name
            session.token = session_cookie_value
            session.user = data.get("user")
        
        return {
            "message": "Successfully logged in",
            "user": session.user,
            "token": session.token
        }
    
    async def whoami(self):

        if not session.token:
            return {"error": "Not logged in"}

        headers = {}

        if session.token:
            headers["Cookie"] = (
                f"{session.cookie_name}={session.token}"
            )

        res = await self.client.get("/api/auth/get-session", headers=headers)
        
        return {
            # "cookie_sent": headers.get("Cookie"),
            "status": res.status_code,
            # "body": res.text
        }

    async def logout(self): 
        if not session.token:
            raise Exception(
                "no user logged in"
            )

        res = await self.client.post("auth/sign-out")
        res.raise_for_status()

        session.token = None
        session.cookie_name = None
        session.user = None

        return "Logged out successfully.."


# ---------------------->>>>>>  EXPENSE SERVICES <<<<---------------------


    async def get_expense(self):
        res = await self.client.get("/transaction")
        res.raise_for_status()
        return res.json()

    async def add_expense(self, data: ExpenseCreate):
        res = await self.client.post("/transaction", json=data.model_dump(mode="json"))
        res.raise_for_status()
        return res.json()

    async def delete_expense(self, id: str):
        res = await self.client.delete(f"/transaction/{id}")
        res.raise_for_status()
        return res.json()
    
    async def edit_expense(self, id: str, data: ExpenseCreate):
        res = await self.client.put(f"/transaction/{id}", json=data.model_dump(mode="json"))
        res.raise_for_status()
        return res.json()