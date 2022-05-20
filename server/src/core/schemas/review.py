from pydantic import BaseModel, conint, constr


class Create_review(BaseModel):
    rate: conint(ge=1, le=5)
    comment: constr(min_length=1, max_length=100)
