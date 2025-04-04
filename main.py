import logging
from fastapi import FastAPI
import uvicorn
from app.utils.cors import setup_cors
from app.utils.openapi_tags import OPENAPI_TAGS
from app.routers.router_a_star import router_a_star
from app.routers.router_clusterization import router_clusterization
from app.routers.router_genetic import router_genetic
from app.routers.router_ant_colony import router_ant_colony
from app.routers.router_tree import router_tree
from app.routers.router_neural_network import router_neural_network


app = FastAPI(
    title="Approximate calculations",
    openapi_tags=OPENAPI_TAGS,
)
setup_cors(app)
logger = logging.getLogger("uvicorn.error")

routers = [
    router_a_star,
    router_clusterization,
    router_genetic,
    router_ant_colony,
    router_tree,
    router_neural_network,
]

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="trace")
