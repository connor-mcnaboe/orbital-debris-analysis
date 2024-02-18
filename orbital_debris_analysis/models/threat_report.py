from pydantic import BaseModel


class ThreatReport(BaseModel):
    total_threat_count: int
    rocket_body_threat_count: int
    debris_threat_count: int
    inactive_sat_threat_count: int
    active_sat_threat_count: int
