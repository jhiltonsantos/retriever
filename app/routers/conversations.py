from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import conversations as conversations_service

router = APIRouter(tags=["conversations"])


class CreateConversationPayload(BaseModel):
    title: str = Field(..., min_length=1)


class AddMessagePayload(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1)
    sources: list | None = None
    agent_steps: list | None = None


class UpdateTitlePayload(BaseModel):
    title: str = Field(..., min_length=1)


@router.get("/conversations")
async def list_conversations():
    return {"conversations": conversations_service.list_conversations()}


@router.post("/conversations")
async def create_conversation(payload: CreateConversationPayload):
    return conversations_service.create_conversation(payload.title)


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    conversation = conversations_service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    deleted = conversations_service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    return {"ok": True}


@router.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, payload: AddMessagePayload):
    conversation = conversations_service.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")

    return conversations_service.add_message(
        conversation_id=conversation_id,
        role=payload.role,
        content=payload.content,
        sources=payload.sources,
        agent_steps=payload.agent_steps,
    )


@router.put("/conversations/{conversation_id}")
async def update_conversation_title(conversation_id: str, payload: UpdateTitlePayload):
    conversation = conversations_service.update_conversation_title(
        conversation_id, payload.title
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    return conversation
