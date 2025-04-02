from fastapi import FastAPI
from app.routers.routes import router
from app.routers.clusterization_router import clusterization_router
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = FastAPI()

setup_cors(app)
app.include_router(router)
app.include_router(clusterization_router)
