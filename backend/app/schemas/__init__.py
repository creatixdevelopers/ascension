from typing import Annotated

from pydantic import BaseModel, ConfigDict, constr


class Model(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, from_attributes=True, populate_by_name=True
    )


Email = Annotated[
    str,
    constr(
        min_length=5,
        max_length=128,
        pattern=r"^\S+@\S+\.\S+$",
        to_lower=True,
        strip_whitespace=True,
    ),
]

Password = Annotated[
    str,
    constr(
        min_length=8,
        max_length=32,
        strip_whitespace=True,
    ),
]
