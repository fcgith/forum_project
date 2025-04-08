from fastapi import FastAPI
from auth import router as auth_router
# from admin import router as admin_router
from categories import router as category_router
from topics import router as topics_router
from posts import router as posts_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.245.56.116:3080"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows OPTIONS, POST, etc.
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
# app.include_router(admin_router, prefix="/admin")
app.include_router(category_router, prefix="/categories")
app.include_router(topics_router, prefix="/topics")
app.include_router(posts_router, prefix="/posts")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)