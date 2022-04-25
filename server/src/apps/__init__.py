from fastapi import APIRouter

from src.apps import auth, content, review, search

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(review.router, prefix="/review", tags=["review"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
