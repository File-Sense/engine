from fastapi import FastAPI
import uvicorn
from sys import argv
global reload_state
if "dev" not in argv:
    import ensure_exit
    reload_state = False
else:
    reload_state = True

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=reload_state)