# app/providers/pluggy_client.py (ou app/integracoes/pluggy_client.py)
import httpx
from typing import Any


class PluggyClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str, timeout: int = 30) -> None:
        self._client = httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=timeout)
        self.client_id = client_id
        self.client_secret = client_secret

    async def close(self) -> None:
        await self._client.aclose()

    # ---------- helpers ----------
    async def _post_json(
        self,
        path: str,
        json: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        r = await self._client.post(path, json=json, headers=headers or {})
        # Em 4xx, deixamos o consumidor tratar (r.json pode trazer erro legível)
        if 500 <= r.status_code:
            r.raise_for_status()
        return r.json()  # type: ignore[no-any-return]

    async def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        r = await self._client.get(path, params=params or {}, headers=headers or {})
        r.raise_for_status()
        return r.json()  # type: ignore[no-any-return]

    # ---------- tokens ----------
    async def auth_token(self) -> str:
        """
        Pede um token de autenticação para a Pluggy.
        Tenta /auth e /auth/token e aceita vários nomes de campo.
        """
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

        async def try_path(path: str, headers: dict[str, str]) -> str | None:
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

    # ---------- data: accounts ----------
    async def list_accounts(self, item_id: str) -> list[dict[str, Any]]:
        """
        Lista as contas vinculadas a um item (instituição conectada).
        """
        api_key = await self.auth_token()
        data = await self._get(
            "/accounts",
            params={"itemId": item_id},
            headers={"X-API-Key": api_key},
        )
        if isinstance(data, list):
            return data
        return data.get("results", [])

    async def get_account(self, account_id: str) -> dict[str, Any]:
        """
        Busca uma conta específica pelo accountId.
        """
        api_key = await self.auth_token()
        data = await self._get(
            f"/accounts/{account_id}",
            params={},
            headers={"X-API-Key": api_key},
        )
        # Aqui a API normalmente retorna um objeto único
        return data

    # ---------- data: transactions ----------
    async def list_transactions(
        self,
        account_id: str,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Lista transações de uma conta.
        from_date/to_date devem estar no formato 'YYYY-MM-DD', se usados.
        """
        api_key = await self.auth_token()
        params: dict[str, Any] = {"accountId": account_id}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        data = await self._get(
            "/transactions",
            params=params,
            headers={"X-API-Key": api_key},
        )

        if isinstance(data, list):
            return data
        return data.get("results", [])

    # ---------- debug ----------
    async def debug_auth(self) -> dict[str, Any]:
        payload = {"clientId": self.client_id, "clientSecret": self.client_secret}
        out: dict[str, Any] = {}
        for path in ("/auth", "/auth/token"):
            try:
                r = await self._client.post(path, json=payload)
                try:
                    body: Any = r.json()
                except Exception:
                    body = r.text
                out[path] = {"status": r.status_code, "body": body}
            except Exception as e:  # pragma: no cover (apenas debug)
                out[path] = {"error": str(e)}
        return out
