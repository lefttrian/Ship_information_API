
import uvicorn
from app.pipeline import process
import os


if __name__ == "__main__":
    process()
    uvicorn.run('app:main.app', reload=True, port=os.environ.get("PORT", 5000), host='0.0.0.0')
