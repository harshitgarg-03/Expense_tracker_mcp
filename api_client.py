import httpx
from config import API_BASE_URL
from session import session
from schemas.expense import ExpenseCreate


class ExpenseApi:
    def __init__(self, token: str | None = None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

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
        # data = res.json()

        # session.token = data.get("token")
        # session.user = data.get("user")

        return {
            "message": "user signup success..",
            # "user": session.user
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
        cookiedata = res.headers.get("set-cookie")
        session.token =  cookiedata.split(";")[0].split("=")[1]
        session.user = data.get("user")
        
        return {
            "message": "Successfully logged in",
            "user": session.token
        }
    
    async def whoami(self):

        res = await self.client.get(
            "/api/auth/get-session",
            headers={
                "Cookie": session.token
            }
        )

        try:
            print("JSON:", res.json(), flush=True)
        except Exception as e:
            print("JSON ERROR:", e, flush=True)

        return {"done": True}


    async def logout(self): 
        if not session.token:
            raise Exception(
                "no user logged in"
            )

        res = await self.client.post(
            "auth/sign-out",
            headers={
                "Authorization": f"Bearer {session.token}"
            }
        )
        res.raise_for_status()

        session.token = None
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