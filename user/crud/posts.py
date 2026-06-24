from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, delete
from fastapi import HTTPException
from settings.database import get_session
from models import Post, PostComment,PostMedia, Privacy, Follower
from user.crud.mongo_likes import remove_post_likes_for_post




async def create_post(user_id: int, caption: str, status="active"):
    async with get_session() as session:
        try:
            new_post = Post(user_id=user_id, caption=caption, status=status)
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
            return new_post
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_posts(requester_id: int):
    async with get_session() as session:
        try:
            result = await session.execute(select(Post))
            posts = result.scalars().all()
            visible_posts = []
            for post in posts:
                priv_result = await session.execute(
                    select(Privacy).where(Privacy.user_id == post.user_id, Privacy.current == True)
                )
                privacy = priv_result.scalars().first()
                if not privacy or privacy.priv_status == "public":
                    visible_posts.append(post)
                elif post.user_id == requester_id:
                    visible_posts.append(post)
                else:
                    follow_result = await session.execute(
                        select(Follower).where(
                            and_(Follower.follower_id == requester_id, Follower.following_id == post.user_id)
                        )
                    )
                    if follow_result.scalars().first():
                        visible_posts.append(post)
            return visible_posts
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def update_post(post_id: int, new_caption: str):
    async with get_session() as session:
        try:
            post = await session.get(Post, post_id)
            if post:
                post.caption = new_caption
                await session.commit()
                return post
            return None
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_post(post_id: int):
    async with get_session() as session:
        try:
            post = await session.get(Post, post_id)
            if post:
                await remove_post_likes_for_post(post_id)
                await session.execute(delete(PostComment).where(PostComment.post_id == post_id))
                await session.execute(delete(PostMedia).where(PostMedia.post_id == post_id))
                await session.delete(post)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def add_post_comment(post_id: int, user_id: int, text: str):
    async with get_session() as session:
        try:
            new_comment = PostComment(post_id=post_id, user_id=user_id, text=text)
            session.add(new_comment)
            await session.commit()
            await session.refresh(new_comment)
            return new_comment
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def delete_post_comment(comment_id: int):
    async with get_session() as session:
        try:
            comment = await session.get(PostComment, comment_id)
            if comment:
                await session.delete(comment)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")




async def add_post_media(post_id: int, media_url: str, media_type: str, order_index: int):
    async with get_session() as session:
        try:
            new_media = PostMedia(post_id=post_id, media_url=media_url, media_type=media_type, order_index=order_index)
            session.add(new_media)
            await session.commit()
            await session.refresh(new_media)
            return new_media
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")


async def remove_post_media(media_id: int):
    async with get_session() as session:
        try:
            media = await session.get(PostMedia, media_id)
            if media:
                await session.delete(media)
                await session.commit()
                return True
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
