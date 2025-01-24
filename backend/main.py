from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging

from .config import settings
from .api import routes
# 配置日志
logging.basicConfig( 
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到终端
        logging.FileHandler('app.log')  # 同时写入文件
    ]
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # 配置 CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # 挂载静态文件
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
    
    # 注册路由
    app.include_router(routes.router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    async def read_root():
        return FileResponse("frontend/templates/index.html")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)