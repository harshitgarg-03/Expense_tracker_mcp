import httpx
from config import API_BASE_URL
from session import session
from schemas.expense import Expense_Create


class ExpenseApi:
    def __init__ (self, token: str | None = None):

        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            timeout=30,
            headers= headers
        )

    async def close(self):
        await self.client.aclose()


# ---------------------->>>>>>  GENERIC METHODS  <<<<---------------------


    async def get(self, path: str):
        res = await self.client.get(path)
        res.raise_for_status()

        return res.json()
    
    async def post(self, path: str, data: dict):
        res = await self.client.post(path, json = data)
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
            f"auth/sign-up/email",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        session.token = res["token"]
        session.user = res["user"]

        return {
            "message": "user signup success..",
            "user": res["user"]
        }

    async def signin_user(self, email: str, password: str):
        res = await self.client.post(
            f"auth/sign-in/email",
            json={
                "email": email,
                "password": password
            }
        )

        if res.status_code != 200:
            return {
                "error": "Invalid credentials"
            }

        session.token = res["token"]
        session.user = res["user"]
        
        return {
            "message": "Successfully logged in",
            "user": res["user"]
        }
    
    async def whoami(self):
        if not session.token :
            return {
                "message" : "not authenticated "
            }
        
        return await self.client.get(
            f"auth/get-session",
            headers={
                "Authorization":
                f"Bearer {session.token}"
            }
        )
    
    async def logout(self): 
        if not session.token:
            raise Exception(
                "no user logged in"
            )

        await self.client.post(
            f"{API_BASE_URL}/auth/sign-out",
            headers={
                "Authorization": f"Bearer {session.token}"
            }
        )

        session.token = None
        session.user = None

        return "Logged out successfully.."


# ---------------------->>>>>>  EXPENSE SERVICES <<<<---------------------


    async def get_expense(self):
        return await self.client.get("/transaction")

    async def add_expense(self, data: Expense_Create):
        return await self.client.post("/transaction", json=data.model_dump(mode="json"))

    async def delete_expense(self, id: str):
        return await self.client.delete("/transaction/{id}")
    
    async def edit_expense(self, id:str, data: Expense_Create):
        return await self.client.put("/transaction/{id}", json=data.model_dump(mode="json"))
    
    # async def get_budget(self):
    #     res = await self.client.get("/budget")
    #     res.raise_for_status()
    #     return res.json()
    
    # async def get_analytics(self):
    #     res = await self.client.get("/analytics")

        res.raise_for_status()
        return res.json()