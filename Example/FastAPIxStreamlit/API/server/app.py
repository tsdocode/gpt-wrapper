from fastapi import FastAPI

from server.routes.GPT import router as GPTRoutes



from starlette.middleware.cors import CORSMiddleware




app = FastAPI()


app.include_router(GPTRoutes, tags=["GPT"], prefix="/gpt")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST","PUT","DELETE", "OPTION", "GET"],
    allow_headers=["*"],
)