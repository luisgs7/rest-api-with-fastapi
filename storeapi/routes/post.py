from fastapi import APIRouter

from storeapi.models.post import UserPost, UserPostIn

router = APIRouter()

post_table = []
@router.get("/")
async def get_root():
    return {"message": "Hello World"}


@router.get("/posts", response_model=list[UserPost])
async def get_all_posts():
    return post_table


@router.post("/posts", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table.append(new_post)
    return new_post