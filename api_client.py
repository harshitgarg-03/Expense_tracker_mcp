import httpx
from config import API_BASE_URL

class ExpenseApi:
    def __inti__ (self, token: str):
        self.client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            timeout=30,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    async def get_expense(self):

        try:
            res = await self.client.get("/api/transaction")
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
        res = await self.client.post("/api/transaction")
        res.raise_for_status()
        return res.json()

    async def delete_expense(self):
        res = await self.client.delete("/api/transaction/{id}")
        res.raise_for_status()
        return res.json()
    
    async def edit_expense(self):
        res = await self.client.put("/api/transaction/{id}")
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