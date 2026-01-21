from pydantic import BaseModel

class FlagSubmitRequest(BaseModel):
    machine_id: str
    flag: str
    user_id: str
