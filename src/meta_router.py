from fastapi import APIRouter
from starlette.status import HTTP_200_OK


router = APIRouter()


@router.get("/_meta/health", status_code=HTTP_200_OK)
async def health_check():
    """
    Status response for readiness and liveness probe
    """
    return {"status": "ok"}
