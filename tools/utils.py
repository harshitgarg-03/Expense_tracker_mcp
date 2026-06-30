from session import session

from api_client import ExpenseApi

def get_api():
    if not session.token:
        raise Exception (
            "please login first "
        )
    
    return ExpenseApi(session.token)