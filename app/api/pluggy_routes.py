# app/integracoes/api/pluggy_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter(prefix="/api/v1/pluggy", tags=["pluggy"])


def get_pluggy(request: Request):
    client = getattr(request.app.state, "pluggy_client", None)
    if not client:
        raise HTTPException(500, "Pluggy client not initialized")
    return client

@router.get("/connect-token")
async def get_connect_token(client = Depends(get_pluggy)):
    try:
        token = await client.create_connect_token()
        return {"connectToken": token}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Connect token error: {e}")

@router.get("/accounts/{item_id}")
async def accounts(item_id: str, client = Depends(get_pluggy)):
    return await client.list_accounts(item_id)

@router.get("/transactions/{account_id}")
async def transactions(account_id: str, client = Depends(get_pluggy)):
    return await client.list_transactions(account_id)

@router.get("/_debug-auth")
async def debug_auth(client = Depends(get_pluggy)):
    return await client.debug_auth()

