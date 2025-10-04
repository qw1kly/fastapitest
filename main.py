from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
import uvicorn


from routes import post
import asyncio




app = FastAPI()
app.include_router(post.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0")
