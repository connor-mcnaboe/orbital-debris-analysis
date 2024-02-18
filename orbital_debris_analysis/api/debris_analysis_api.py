from fastapi import APIRouter
from orbital_debris_analysis.models.mission import Mission
from orbital_debris_analysis.models.threat_report import ThreatReport
from orbital_debris_analysis.debris_analysis.debris_analysis import extract_analysis_data, calculate_threat_model
from orbital_debris_analysis.csv_parser.csv_parser import csv_to_pandas

router = APIRouter()


@router.get("/threat-report/")
async def read_threat_report(mission: Mission) -> ThreatReport:
    full_data_frame = csv_to_pandas("./orbital_debris_analysis/data/SATCAT.csv")
    extracted_data_frame = extract_analysis_data(data_frame=full_data_frame)
    return calculate_threat_model(data_frame=extracted_data_frame, mission=mission)
