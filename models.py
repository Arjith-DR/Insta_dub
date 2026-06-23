from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from settings.database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, nullable=False)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String)
    email = Column(String)
    phone = Column(String)
    profile_pic = Column(String)

    bios = relationship("Bio", back_populates="user")
    privacies = relationship("Privacy", back_populates="user")
    posts = relationship("Post", back_populates="user")
    reels = relationship("Reel", back_populates="user")
    saved_categories = relationship("SavedCategory", back_populates="user")
    saved_items = relationship("SavedItem", back_populates="user")
    password_changes = relationship("PasswordChange", back_populates="user")
    followers = relationship("Follower", foreign_keys="[Follower.follower_id]", back_populates="follower")
    following = relationship("Follower", foreign_keys="[Follower.following_id]", back_populates="following")
    user_roles = relationship("UserRole", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String)
    description = Column(Text)

    user_roles = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_role"

    user_role_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


class Bio(Base):
    __tablename__ = "bio"

    bio_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    b_txt = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    current = Column(Boolean)

    user = relationship("User", back_populates="bios")


class Username(Base):
    __tablename__ = "username"

    user_name_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user_status = Column(String, unique=True)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    current = Column(Boolean)


class Privacy(Base):
    __tablename__ = "privacy"

    priv_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    priv_status = Column(String)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    current = Column(Boolean)

    user = relationship("User", back_populates="privacies")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    caption = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String)

    user = relationship("User", back_populates="posts")
    media = relationship("PostMedia", back_populates="post")
    comments = relationship("PostComment", back_populates="post")
    likes = relationship("PostLike", back_populates="post")


class PostMedia(Base):
    __tablename__ = "post_media"

    media_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    media_url = Column(String)
    media_type = Column(String)
    order_index = Column(Integer)

    post = relationship("Post", back_populates="media")


class Reel(Base):
    __tablename__ = "reels"

    reel_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    video_url = Column(String)
    caption = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String)

    user = relationship("User", back_populates="reels")
    comments = relationship("ReelComment", back_populates="reel")
    likes = relationship("ReelLike", back_populates="reel")


class PostComment(Base):
    __tablename__ = "post_comments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    text = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    post = relationship("Post", back_populates="comments")


class ReelComment(Base):
    __tablename__ = "reel_comments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    reel_id = Column(Integer, ForeignKey("reels.reel_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    text = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    reel = relationship("Reel", back_populates="comments")


class PostLike(Base):
    __tablename__ = "post_likes"
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_post_like"),)

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    is_liked = Column(Boolean)

    post = relationship("Post", back_populates="likes")


class ReelLike(Base):
    __tablename__ = "reel_likes"
    __table_args__ = (UniqueConstraint("reel_id", "user_id", name="unique_reel_like"),)

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    reel_id = Column(Integer, ForeignKey("reels.reel_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    is_liked = Column(Boolean)

    reel = relationship("Reel", back_populates="likes")


class SavedCategory(Base):
    __tablename__ = "saved_categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="saved_categories")
    items = relationship("SavedItem", back_populates="category")


class Content(Base):
    __tablename__ = "content"

    content_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    type = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String)


class SavedItem(Base):
    __tablename__ = "saved_items"

    saved_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.content_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("saved_categories.category_id"))
    saved_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    is_saved = Column(Boolean)

    user = relationship("User", back_populates="saved_items")
    category = relationship("SavedCategory", back_populates="items")


class PasswordChange(Base):
    __tablename__ = "password_changes"

    change_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    old_password = Column(String)
    new_password = Column(String)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="password_changes")


class Follower(Base):
    __tablename__ = "followers"
    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="unique_follow"),
        CheckConstraint("follower_id != following_id", name="no_self_follow"),
    )

    follow_id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    following_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    follower = relationship("User", foreign_keys=[follower_id], back_populates="followers")
    following = relationship("User", foreign_keys=[following_id], back_populates="following")



class AdminPrivacyOverride(Base):
    __tablename__ = "admin_privacy_overrides"

    override_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=True)  # null = global policy
    policy_name = Column(String, nullable=True)
    policy_value = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)