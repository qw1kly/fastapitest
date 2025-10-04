from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
import uvicorn


from routes import post

from contextlib import asynccontextmanager
import asyncio
from background_tasks import run_background_tasks

background_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global background_task
    background_task = asyncio.create_task(run_background_tasks())
    yield
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass



app = FastAPI(lifespan=lifespan)
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