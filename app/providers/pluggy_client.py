# app/integracoes/pluggy_client.py
import httpx
from typing import Any

class PluggyClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str, timeout: int = 30):
        self._client = httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=timeout)
        self.client_id = client_id
        self.client_secret = client_secret

    async def close(self):
        await self._client.aclose()

    # ---------- helpers ----------
    async def _post_json(self, path: str, json: dict, headers: dict | None = None) -> dict:
        r = await self._client.post(path, json=json, headers=headers or {})
        if 500 <= r.status_code:
            r.raise_for_status()
        return r.json()

    async def _get(self, path: str, params: dict | None = None, headers: dict | None = None) -> dict:
        r = await self._client.get(path, params=params or {}, headers=headers or {})
        r.raise_for_status()
        return r.json()

    # ---------- tokens ----------
    async def auth_token(self) -> str:
        payload = {"clientId": self.client_id, "clientSecret": self.client_secret}
        for path in ("/auth", "/auth/token"):
            data = await self._post_json(path, payload)
            for k in ("apiKey", "accessToken", "access_token"):
                v = data.get(k)
                if isinstance(v, str) and v:
                    return v
        raise RuntimeError("Auth failed: no apiKey/accessToken from /auth or /auth/token")

    async def create_connect_token(self) -> str:
        """
        Gera o token para o Pluggy Connect. Alguns ambientes devolvem 'connectToken',
        outros 'token' ou até 'accessToken'. Tornamos tolerante e normalizamos.
        """
        api_key = await self.auth_token()

        async def try_path(path: str, headers: dict) -> str | None:
            data = await self._post_json(path, {}, headers=headers)
            for k in ("connectToken", "token", "accessToken", "access_token"):
                v = data.get(k)
                if isinstance(v, str) and v:
                    return v
            return None

        # Preferência: X-API-Key
        for path in ("/connect_token", "/connect/token"):
            tok = await try_path(path, {"X-API-Key": api_key})
            if tok:
                return tok
        # Fallback: Bearer
        for path in ("/connect_token", "/connect/token"):
            tok = await try_path(path, {"Authorization": f"Bearer {api_key}"})
            if tok:
                return tok
        # Última carta: usar a própria apiKey
        return api_key

    # ---------- data ----------
    async def list_accounts(self, item_id: str) -> list[dict[str, Any]]:
        api_key = await self.auth_token()
        data = await self._get("/accounts", params={"itemId": item_id}, headers={"X-API-Key": api_key})
        return data.get("results", data if isinstance(data, list) else [])

    async def list_transactions(self, account_id: str) -> list[dict]:
        api_key = await self.auth_token()
        data = await self._get("/transactions", params={"accountId": account_id}, headers={"X-API-Key": api_key})
        return data.get("results", data if isinstance(data, list) else [])
    
    async def debug_auth(self) -> dict:
        payload = {"clientId": self.client_id, "clientSecret": self.client_secret}
        out = {}
        for path in ("/auth", "/auth/token"):
            try:
                r = await self._client.post(path, json=payload)
                try:
                    body = r.json()
                except Exception:
                    body = r.text
                out[path] = {"status": r.status_code, "body": body}
            except Exception as e:
                out[path] = {"error": str(e)}
        return out

