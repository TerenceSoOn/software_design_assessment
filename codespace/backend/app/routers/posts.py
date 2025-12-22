"""
Posts router - Public Square functionality.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.post import Post, PostLike, PostComment
from app.schemas.post import PostCreate, PostResponse, CommentCreate, CommentResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post."""
    new_post = Post(
        user_id=current_user.id,
        content_text=post_data.content_text,
        image_urls=post_data.image_urls,
        tags=post_data.tags
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # Get author profile
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    # Add counts and author info
    response = PostResponse.model_validate(new_post)
    response.like_count = 0
    response.comment_count = 0
    response.author_name = profile.display_name if profile else current_user.username
    response.author_avatar_url = profile.avatar_url if profile else None
    
    return response


@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all posts (feed)."""
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    # Add counts and author info for each post
    result = []
    for post in posts:
        # Get author profile
        profile = db.query(Profile).filter(Profile.user_id == post.user_id).first()
        
        response = PostResponse.model_validate(post)
        response.like_count = db.query(PostLike).filter(PostLike.post_id == post.id).count()
        response.comment_count = db.query(PostComment).filter(PostComment.post_id == post.id).count()
        response.author_name = profile.display_name if profile else f"User #{post.user_id}"
        response.author_avatar_url = profile.avatar_url if profile else None
        result.append(response)
    
    return result


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like a post."""
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing_like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")
    
    # Create like
    new_like = PostLike(post_id=post_id, user_id=current_user.id)
    db.add(new_like)
    db.commit()
    
    return {"message": "Post liked"}


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unlike a post."""
    like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(like)
    db.commit()
    
    return None


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a post."""
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create comment
    new_comment = PostComment(
        post_id=post_id,
        user_id=current_user.id,
        comment_text=comment_data.comment_text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Get author profile
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    response = CommentResponse.model_validate(new_comment)
    response.author_name = profile.display_name if profile else current_user.username
    response.author_avatar_url = profile.avatar_url if profile else None
    
    return response


@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Get all comments for a post."""
    comments = db.query(PostComment).filter(
        PostComment.post_id == post_id
    ).order_by(PostComment.created_at).all()
    
    result = []
    for comment in comments:
        profile = db.query(Profile).filter(Profile.user_id == comment.user_id).first()
        response = CommentResponse.model_validate(comment)
        response.author_name = profile.display_name if profile else f"User #{comment.user_id}"
        response.author_avatar_url = profile.avatar_url if profile else None
        result.append(response)
    
    return result
