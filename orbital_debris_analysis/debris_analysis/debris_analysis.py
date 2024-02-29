import math

import pandas as pd
from pandas import DataFrame
from datetime import datetime

from orbital_debris_analysis.csv_parser.csv_parser import csv_to_pandas
from orbital_debris_analysis.models.mission import Mission
from orbital_debris_analysis.models.object_type_enum import ObjectTypeEnum
from orbital_debris_analysis.models.status_enum import StatusEnum
from orbital_debris_analysis.models.threat_report import ThreatReport

# Minimum Columns needed for Analysis #
INTLDES = "INTLDES"
OBJECT_TYPE = "OBJECT_TYPE"
DECAY = "DECAY"
APOGEE = "APOGEE"
PERIGEE = "PERIGEE"

# Minimum Columns needed for status lookup
STATUS = "Status"


def extract_analysis_data(data_frame: DataFrame):
    return data_frame[[INTLDES, OBJECT_TYPE, DECAY, APOGEE, PERIGEE]]


def extract_status_data(data_frame: DataFrame):
    return data_frame[[INTLDES, STATUS]]


def calculate_threat_model(mission: Mission) -> ThreatReport:
    full_data_frame = csv_to_pandas("./orbital_debris_analysis/data/SATCAT.csv")
    full_status_data_frame = csv_to_pandas("./orbital_debris_analysis/data/active_data_sheet.csv")

    extracted_data_frame = extract_analysis_data(data_frame=full_data_frame)
    extracted_status_data_frame = extract_status_data(data_frame=full_status_data_frame)

    threat_report = ThreatReport(total_threat_count=0,
                                 rocket_body_threat_count=0,
                                 debris_threat_count=0,
                                 inactive_sat_threat_count=0,
                                 active_sat_threat_count=0)
    for index, row in extracted_data_frame.iterrows():
        if is_orbital(row):
            if is_in_mission_vicinity(debris_apogee=row[APOGEE], debris_perigee=row[PERIGEE], mission=mission):
                # Increment overall threat count
                threat_report.total_threat_count += 1
                # Determine object type:
                match row[OBJECT_TYPE]:
                    case ObjectTypeEnum.DEBRIS.value:
                        threat_report.debris_threat_count += 1
                    case ObjectTypeEnum.ROCKET_BODY.value:
                        threat_report.rocket_body_threat_count += 1
                    case ObjectTypeEnum.PAYLOAD.value:
                        for status_index, status_row in extracted_status_data_frame.iterrows():
                            if status_row[INTLDES] == row[INTLDES]:
                                if status_row[STATUS] == StatusEnum.ACTIVE.value:
                                    threat_report.active_sat_threat_count += 1
                                elif status_row[STATUS] == StatusEnum.INACTIVE.value:
                                    threat_report.inactive_sat_threat_count += 1
                    case ObjectTypeEnum.UNKNOWN.value:
                        # TODO: Determine how to treat unknown bodies
                        pass
    return threat_report


def is_orbital(row) -> bool:
    return isinstance(row[DECAY], float) and math.isnan(row[DECAY])


def is_in_mission_vicinity(debris_apogee: int, debris_perigee: int, mission: Mission) -> bool:
    if math.isnan(debris_apogee) or math.isnan(debris_perigee):
        return False
    # Apogee upper and lower bounds check data
    mission_apogee_upper_tol = mission.apogee + mission.threat_tolerance_km
    mission_apogee_lower_tol = mission.apogee - mission.threat_tolerance_km
    # Perigee upper and lower bounds check data
    mission_perigee_upper_tol = mission.perigee + mission.threat_tolerance_km
    mission_perigee_lower_tol = mission.perigee - mission.threat_tolerance_km

    if debris_apogee >= mission_apogee_lower_tol and debris_perigee <= mission_perigee_lower_tol:
        return True

    return False
