from fastapi import FastAPI, Response, Header, HTTPException
 
app = FastAPI()

@app.get("/headers")
def root(accept_language: str = Header(), user_agent: str = Header()):
    if user_agent is None or accept_language is None:
        raise HTTPException(status_code=400, detail="Missing required headers")
    return {"Accept_Language": accept_language,
            "User_Agent": user_agent}