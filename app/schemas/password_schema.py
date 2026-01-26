from pydantic import BaseModel

class PasswordResetRequest(BaseModel):
    current_password: str
    new_password: str

