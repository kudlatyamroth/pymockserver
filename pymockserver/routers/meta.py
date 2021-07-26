from fastapi import APIRouter
from starlette.status import HTTP_200_OK

router = APIRouter(tags=["Meta"])


@router.get("/_meta/health", status_code=HTTP_200_OK)
def health_check() -> dict[str, str]:
    """
    Status response for readiness and liveness probe
    """
    return {"status": "ok"}
