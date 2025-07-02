from typing import Optional
import aiohttp


class BaseRouter:
    def __init__(self, session: aiohttp.ClientSession, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip('/')
    
    async def _get(self, path: str, params: Optional[dict] = None):
        """Perform a GET request and return JSON response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with self.session.get(url, params=params) as response:
            if not response.ok:
                try:
                    error_detail = await response.json()
                    # Extract the actual error message from various possible fields
                    if isinstance(error_detail, dict):
                        if 'detail' in error_detail:
                            error_message = error_detail['detail']
                        elif 'message' in error_detail:
                            error_message = error_detail['message']
                        elif 'error' in error_detail:
                            error_message = error_detail['error']
                        else:
                            error_message = str(error_detail)
                    elif isinstance(error_detail, list) and error_detail:
                        # Handle validation errors that come as a list
                        error_message = "; ".join(str(item) for item in error_detail)
                    else:
                        error_message = str(error_detail)
                    
                    raise aiohttp.ClientResponseError(
                        response.request_info, 
                        response.history,
                        status=response.status,
                        message=error_message,
                        headers=response.headers
                    )
                except aiohttp.ClientResponseError:
                    # Re-raise our custom error
                    raise
                except Exception:
                    # Fallback if we can't parse JSON
                    try:
                        error_text = await response.text()
                        error_message = error_text or f"HTTP {response.status}: {response.reason}"
                    except:
                        error_message = f"HTTP {response.status}: {response.reason}"
                    
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response.history,
                        status=response.status,
                        message=error_message,
                        headers=response.headers
                    )
            return await response.json()
    
    async def _post(self, path: str, json: Optional[dict] = None, params: Optional[dict] = None) -> dict:
        """Perform a POST request and return JSON response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with self.session.post(url, json=json, params=params) as response:
            if not response.ok:
                try:
                    error_detail = await response.json()
                    # Extract the actual error message from various possible fields
                    if isinstance(error_detail, dict):
                        if 'detail' in error_detail:
                            error_message = error_detail['detail']
                        elif 'message' in error_detail:
                            error_message = error_detail['message']
                        elif 'error' in error_detail:
                            error_message = error_detail['error']
                        else:
                            error_message = str(error_detail)
                    elif isinstance(error_detail, list) and error_detail:
                        # Handle validation errors that come as a list
                        error_message = "; ".join(str(item) for item in error_detail)
                    else:
                        error_message = str(error_detail)
                    
                    raise aiohttp.ClientResponseError(
                        response.request_info, 
                        response.history,
                        status=response.status,
                        message=error_message,
                        headers=response.headers
                    )
                except aiohttp.ClientResponseError:
                    # Re-raise our custom error
                    raise
                except Exception:
                    # Fallback if we can't parse JSON - try to get text content
                    try:
                        error_text = await response.text()
                        error_message = error_text or f"HTTP {response.status}: {response.reason}"
                    except:
                        error_message = f"HTTP {response.status}: {response.reason}"
                    
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response.history,
                        status=response.status,
                        message=error_message,
                        headers=response.headers
                    )
            response.raise_for_status()
            return await response.json()
    
    async def _delete(self, path: str, params: Optional[dict] = None) -> dict:
        """Perform a DELETE request and return JSON response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with self.session.delete(url, params=params) as response:
            if not response.ok:
                try:
                    error_detail = await response.json()
                    # Extract the actual error message from various possible fields
                    if isinstance(error_detail, dict):
                        if 'detail' in error_detail:
                            error_message = error_detail['detail']
                        elif 'message' in error_detail:
                            error_message = error_detail['message']
                        elif 'error' in error_detail:
                            error_message = error_detail['error']
                        else:
                            error_message = str(error_detail)
                    elif isinstance(error_detail, list) and error_detail:
                        # Handle validation errors that come as a list
                        error_message = "; ".join(str(item) for item in error_detail)
                    else:
                        error_message = str(error_detail)
                    
                    raise aiohttp.ClientResponseError(
                        response.request_info, 
                        response.history,
                        status=response.status,
                        message=error_message,
                        headers=response.headers
                    )
                except aiohttp.ClientResponseError:
                    # Re-raise our custom error
                    raise
                except Exception:
                    # Fallback if we can't parse JSON
                    try:
                        error_text = await response.text()
                        error_message = error_text or f"HTTP {response.status}: {response.reason}"
                    except:
                        error_message = f"HTTP {response.status}: {response.reason}"
                    
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response.history,
                        status=response.status,
                        message=error_message,
                        headers=response.headers
                    )
            return await response.json()