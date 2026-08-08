from fastapi import APIRouter
from pydantic import BaseModel

from app.services import profile as profile_service

router = APIRouter(tags=["profile"])


class UpdateProfilePayload(BaseModel):
    display_name: str | None = None


@router.get("/profile")
async def get_profile():
    return profile_service.get_profile()


@router.put("/profile")
async def update_profile(payload: UpdateProfilePayload):
    return profile_service.update_profile(payload.display_name)
