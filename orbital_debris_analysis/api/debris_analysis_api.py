from fastapi import APIRouter
from orbital_debris_analysis.models.mission import Mission
from orbital_debris_analysis.models.threat_report import ThreatReport
from orbital_debris_analysis.debris_analysis.debris_analysis import calculate_threat_model

router = APIRouter()


@router.post("/threat-report/")
async def read_threat_report(mission: Mission) -> ThreatReport:
    return calculate_threat_model(mission=mission)
