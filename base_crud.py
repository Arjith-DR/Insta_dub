from user.crud.users import create_user, get_users, get_user_by_id, update_user_status, delete_user, change_password, change_username, get_usernames, get_username_by_status
from user.crud.bios import create_bio, update_bio, delete_bio
from user.crud.posts import create_post, get_posts, update_post, delete_post, add_post_comment, delete_post_comment, like_post, unlike_post, add_post_media, remove_post_media
from user.crud.reels import create_reel, get_reels, update_reel, delete_reel, add_reel_comment, delete_reel_comment, like_reel, unlike_reel
from user.crud.followers import follow_user, get_followers, get_following, unfollow_user
from core.crud.saved import create_saved_category, get_saved_categories, add_saved_item, remove_saved_item
from core.crud.content import create_content, get_content, get_content_by_id, update_content, delete_content
from core.crud.privacy import update_privacy, get_privacies, log_password_change, get_password_changes

ACTION_MAP = {
    "user": {
        "create": create_user,
        "get_all": get_users,
        "get_by_id": get_user_by_id,
        "update_status": update_user_status,
        "delete": delete_user,
        "change_password": change_password,
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
        "update": update_post,
        "delete": delete_post,
        "comment": add_post_comment,
        "delete_comment": delete_post_comment,
        "like": like_post,
        "unlike": unlike_post,
        "add_media": add_post_media,
        "remove_media": remove_post_media,
    },
    "reel": {
        "create": create_reel,
        "get_all": get_reels,
        "update": update_reel,
        "delete": delete_reel,
        "comment": add_reel_comment,
        "delete_comment": delete_reel_comment,
        "like": like_reel,
        "unlike": unlike_reel,
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
        raise ValueError(f"No CRUD entity found for {entity}")
    func = entity_map.get(action)
    if not func:
        raise ValueError(f"No action '{action}' found for entity '{entity}'")
    return await func(*args, **kwargs)
