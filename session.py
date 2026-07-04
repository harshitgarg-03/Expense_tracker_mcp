
# mcp session token stored here ..
class SessionStore :
    
    def __init__(self):
        self.token = None # cookie stored 
        self.cookie_name = None
        self.user = None

        
session = SessionStore()