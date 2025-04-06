from fastapi import FastAPI
from auth import router as auth_router
from admin import router as admin_router
from categories import router as category_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")
app.include_router(category_router, prefix="/category")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)