from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse
import logging
from pathlib import Path

from ..services.image_client import ImageServiceClient


image_service = ImageServiceClient(
    "http://localhost:9758",
    "hsyzhendeshuai"
)


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/process")
async def process_image(
    image: UploadFile = File(...),
):
    """处理上传图片"""
    try:
        # 验证文件大小
        image_data = await image.read()
        # 添加文件大小日志
        logger.info(f"Processing file: {image.filename}, size: {len(image_data)}")


        result = await image_service.remove_background(
            image_data,
            image.filename
        )

        if result is None:
            logger.error("Image processing failed")
            raise HTTPException(status_code=500, detail="Image processing failed")
        
        return Response(
            content=result,
            media_type="image/png"
        )

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")