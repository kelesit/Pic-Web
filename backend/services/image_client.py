import aiohttp
from typing import Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ImageServiceClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {"X-API-Key": api_key}

    async def remove_background(self, image_data: bytes, filename: str) -> Optional[bytes]:
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field(
                'image',
                image_data,
                filename=filename,
                content_type='image/png'
            )
            
            try:
                async with session.post(
                    f"{self.base_url}/api/process/remove-background",
                    data=data,
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        error_text = await response.text()
                        logger.error(f"Image processing failed: {error_text}")
                        return None
            except Exception as e:
                logger.error(f"Failed to communicate with image service: {str(e)}")
                raise