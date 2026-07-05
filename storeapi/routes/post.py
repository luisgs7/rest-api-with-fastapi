from tokenize import Comment
from fastapi import APIRouter, HTTPException

from storeapi.models.comments import Comment, CommentIn, UserPostWithComments
from storeapi.models.post import UserPost, UserPostIn

router = APIRouter()


post_table = []
comment_table = []

def find_post(post_id: int):
    return post_table.get(post_id)


@router.get("/")
async def get_root():
    return {"message": "Hello World"}




@router.post("/posts", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table.append(new_post)
    return new_post


@router.get("/posts", response_model=list[UserPost], status_code=200)
async def get_all_posts():
    return post_table


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment], status_code=200)
async def get_comments(post_id: int):
    return [
        comment for comment in comment_table if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments, status_code=200)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "post": post,
        "comments": [
            comment for comment in comment_table if comment["post_id"] == post_id
        ]
    }
