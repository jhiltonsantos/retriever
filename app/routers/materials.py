from fastapi import APIRouter, HTTPException

from app.services import materials as materials_service

router = APIRouter(tags=["materials"])


@router.get("/materials")
async def list_materials():
    return {"materials": materials_service.list_materials()}


@router.delete("/materials/{material_id}")
async def delete_material(material_id: str):
    deleted = materials_service.delete_material(material_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Material não encontrado.")
    return {"ok": True}
