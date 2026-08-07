from fastapi import APIRouter, Form, HTTPException

from app.providers.base import ProviderConfigError, ProviderRequestError
from app.services.rag import ask_question

router = APIRouter(tags=["ask"])


@router.post("/ask")
async def ask(question: str = Form(...)):
    try:
        result = ask_question(question)
    except ProviderConfigError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ProviderRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Modelos indisponíveis. Verifique se o app está rodando na bandeja.",
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar aos modelos em localhost:11434.",
        ) from exc

    response = {"answer": result["answer"]}
    if result["sources"]:
        response["sources"] = result["sources"]
    if result["agent_steps"]:
        response["agent_steps"] = result["agent_steps"]
    return response
