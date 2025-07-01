from typing import Optional
import aiohttp


class BaseRouter:
    def __init__(self, session: aiohttp.ClientSession, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip('/')
    
    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        """Perform a GET request and return JSON response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def _post(self, path: str, json: Optional[dict] = None) -> dict:
        """Perform a POST request and return JSON response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with self.session.post(url, json=json) as response:
            response.raise_for_status()
            return await response.json()
    
    async def _delete(self, path: str, params: Optional[dict] = None) -> dict:
        """Perform a DELETE request and return JSON response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with self.session.delete(url, params=params) as response:
            response.raise_for_status()
            return await response.json()