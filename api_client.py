import httpx
from config import API_BASE_URL
from session import session


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
    
    async def post(self, path: str, data: dict, ):
        res = await self.client.post(path, json = data)
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

        res.raise_for_status()

        data = res.json()
        session.token = data["token"]
        session.user = data["user"]

        return {
            "message": "user signup success..",
            "user": data["user"]
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
        res.raise_for_status()

        data = res.json()

        session.token = data["token"]
        session.user = data["user"]
        
        return {
            "message": "Successfully logged in",
            "user": data["user"]
        }
    
    async def whoami(self):
        if not session.token :
            return {
                "message" : "not authenticated "
            }
        
        res = await self.client.get(
            f"auth/get-session",
            headers={
                "Authorization":
                f"Bearer {session.token}"
            }
        )

        res.raise_for_status()
        return res.json()
    
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

        try:
            res = await self.client.get("/transaction")
            res.raise_for_status()
            return res.json()
        
        except httpx.HTTPStatusError as e:

            if e.response.status_code == 401:
                return {
                    "error": (
                        "You are not logged in. "
                        "Please sign up or log in to use the expense tracker."
                    )
                }

            raise

    async def add_expense(self):
        res = await self.client.post("/transaction")
        res.raise_for_status()
        return res.json()

    async def delete_expense(self):
        res = await self.client.delete("/transaction/{id}")
        res.raise_for_status()
        return res.json()
    
    async def edit_expense(self):
        res = await self.client.put("/transaction/{id}")
        res.raise_for_status()
        return res.json()
    
    # async def get_budget(self):
    #     res = await self.client.get("/budget")
    #     res.raise_for_status()
    #     return res.json()
    
    # async def get_analytics(self):
    #     res = await self.client.get("/analytics")

        res.raise_for_status()
        return res.json()