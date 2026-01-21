from pydantic import BaseModel
from typing import Optional

class CampaignCreateRequest(BaseModel):
    user_id: str
    campaign_name: str
    difficulty: int = 2
    count: Optional[int] = None

