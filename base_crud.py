from user.crud.users import create_user, get_users, get_user_by_id, update_user_status, delete_user, change_password, change_username, get_usernames, get_username_by_status, update_profile_pic
from user.crud.bios import create_bio, update_bio, delete_bio
from user.crud.posts import create_post, get_posts, get_posts_by_user, update_post, delete_post, add_post_comment, delete_post_comment,  add_post_media, remove_post_media
from user.crud.reels import create_reel, get_reels, get_reels_by_user, update_reel, delete_reel, add_reel_comment, delete_reel_comment
from user.crud.followers import follow_user, get_followers, get_following, unfollow_user
from core.crud.saved import create_saved_category, get_saved_categories, add_saved_item, remove_saved_item
from core.crud.content import create_content, get_content, get_content_by_id, update_content, delete_content
from core.crud.privacy import update_privacy, get_privacies, log_password_change, get_password_changes
from user.crud.pg_likes import (
    record_post_like, remove_post_like, get_post_like_details,
    record_reel_like, remove_reel_like, get_reel_like_details
)
from fastapi import HTTPException

ACTION_MAP = {
    "user": {
        "create": create_user,
        "get_all": get_users,
        "get_by_id": get_user_by_id,
        "update_status": update_user_status,
        "delete": delete_user,
        "change_password": change_password,
        "update_profile_pic": update_profile_pic,
    },
    "bio": {
        "create": create_bio,
        "update": update_bio,
        "delete": delete_bio,
    },
    "username": {
        "change": change_username,
        "get_all": get_usernames,
        "get_by_status": get_username_by_status,
    },
    "privacy": {
        "update": update_privacy,
        "get_all": get_privacies,
    },
    "post": {
        "create": create_post,
        "get_all": get_posts,
        "get_by_user": get_posts_by_user,
        "update": update_post,
        "delete": delete_post,
        "comment": add_post_comment,
        "delete_comment": delete_post_comment,
        "like": record_post_like,
        "unlike": remove_post_like,
        "like_details": get_post_like_details,
        "add_media": add_post_media,
        "remove_media": remove_post_media,
    },
    "reel": {
        "create": create_reel,
        "get_all": get_reels,
        "get_by_user": get_reels_by_user,
        "update": update_reel,
        "delete": delete_reel,
        "comment": add_reel_comment,
        "delete_comment": delete_reel_comment,
        "like": record_reel_like,
        "unlike": remove_reel_like,
        "like_details": get_reel_like_details,
    },
    "saved_category": {
        "create": create_saved_category,
        "get_all": get_saved_categories,
    },
    "saved_item": {
        "add": add_saved_item,
        "remove": remove_saved_item,
    },
    "content": {
        "create": create_content,
        "get_all": get_content,
        "get_by_id": get_content_by_id,
        "update": update_content,
        "delete": delete_content,
    },
    "password_change": {
        "log": log_password_change,
        "get_all": get_password_changes,
    },
    "follower": {
        "follow": follow_user,
        "get_followers": get_followers,
        "get_following": get_following,
        "unfollow": unfollow_user,
    },
}

async def dispatch(entity: str, action: str, *args, **kwargs):
    entity_map = ACTION_MAP.get(entity)
    if not entity_map:
        raise HTTPException(status_code=400, detail=f"No CRUD entity found for {entity}")
    func = entity_map.get(action)
    if not func:
        raise HTTPException(status_code=400, detail=f"No action '{action}' found for entity '{entity}'")
    return await func(*args, **kwargs)
