from jwt import encode,decode

def create_token(data : dict) -> str:
    token: str = encode(payload=data,key="pass_key",algorithm="HS256")
    return token

def valid_token(token : str) -> dict:
    data : dict = decode(token,key="pass_key",algorithms=["HS256"])
    return data
    
    
    