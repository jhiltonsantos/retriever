from fastapi import APIRouter

from app.services import graph as graph_service

router = APIRouter(tags=["materials"])


@router.get("/materials/graph")
async def get_materials_graph():
    return graph_service.build_materials_graph()
