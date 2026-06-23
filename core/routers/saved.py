from fastapi import APIRouter, HTTPException
from base_crud import dispatch
from core.schemas import SavedCategoryCreate, SavedCategoryOut, SavedItemCreate, SavedItemOut


saved_router = APIRouter(prefix="/saved", tags=["saved"])


@saved_router.post("/categories", response_model=SavedCategoryOut)
async def create_saved_category(category: SavedCategoryCreate):
    return await dispatch("saved_category", "create", category.user_id, category.name)


@saved_router.get("/categories/{user_id}", response_model=list[SavedCategoryOut])
async def get_saved_categories(user_id: int):
    return await dispatch("saved_category", "get_all", user_id)


@saved_router.post("/items", response_model=SavedItemOut)
async def add_saved_item(item: SavedItemCreate):
    content = await dispatch("content", "get_by_id", item.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return await dispatch("saved_item", "add", item.user_id, item.content_id, item.category_id)


@saved_router.delete("/items/{saved_id}")
async def remove_saved_item(saved_id: int):
    deleted = await dispatch("saved_item", "remove", saved_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Saved item not found")
    return {"detail": "Saved item removed"}
