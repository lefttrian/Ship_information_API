
import uvicorn
from app.pipeline import process


if __name__ == "__main__":
    process()
    uvicorn.run('app:main.app', reload=True, port=8000, host='0.0.0.0')
