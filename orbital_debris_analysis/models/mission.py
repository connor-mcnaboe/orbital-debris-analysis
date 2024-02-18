from pydantic import BaseModel


class Mission(BaseModel):
    apogee: int
    perigee: int
    threat_tolerance_km: int
