"""There you can start FastApi server."""


from api import app
import uvicorn
from config import HOST, PORT

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
