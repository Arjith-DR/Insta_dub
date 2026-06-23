from pydantic import BaseModel

class FollowerOut(BaseModel):
    follow_id: int
    follower_id: int
    following_id: int

    class Config:
        from_attributes = True
