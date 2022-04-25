from pydantic import BaseModel, EmailStr, constr


class Sign_up(BaseModel):
    email: EmailStr
    password: constr(min_length=4)
    nickname: constr(min_length=1, max_length=10)


class Sign_in(BaseModel):
    email: EmailStr
    password: constr(min_length=4)
