import math

import pandas as pd
from pandas import DataFrame
from datetime import datetime

from orbital_debris_analysis.models.mission import Mission
from orbital_debris_analysis.models.object_type_enum import ObjectTypeEnum
from orbital_debris_analysis.models.threat_report import ThreatReport

# Minimum Columns needed for Analysis #
INTLDES = "INTLDES"
OBJECT_TYPE = "OBJECT_TYPE"
DECAY = "DECAY"
APOGEE = "APOGEE"
PERIGEE = "PERIGEE"


def extract_analysis_data(data_frame: DataFrame):
    return data_frame[[INTLDES, OBJECT_TYPE, DECAY, APOGEE, PERIGEE]]


def calculate_threat_model(data_frame: DataFrame, mission: Mission) -> ThreatReport:
    threat_report = ThreatReport(total_threat_count=0,
                                 rocket_body_threat_count=0,
                                 debris_threat_count=0,
                                 inactive_sat_threat_count=0,
                                 active_sat_threat_count=0)

    for index, row in data_frame.iterrows():
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
                        # TODO: Parse .sd file and lookup satellite active vs. inactive
                        pass
                    case ObjectTypeEnum.UNKNOWN.value:
                        # TODO: Determine how to treat unknown bodies
                        pass
    return threat_report


def is_orbital(row) -> bool:
    return isinstance(row[DECAY], float) and math.isnan(row[DECAY])


# return ((row[DECAY] is not None or not math.isnan(row[DECAY])) and
#         datetime.strptime(str(row[DECAY]), "%Y-%m-%d").date() < datetime.now().date())


def is_in_mission_vicinity(debris_apogee: int, debris_perigee: int, mission: Mission) -> bool:
    if math.isnan(debris_apogee) or math.isnan(debris_perigee):
        return False
    # Apogee upper and lower bounds check data
    mission_apogee_upper_tol = mission.apogee + mission.threat_tolerance_km
    mission_apogee_lower_tol = mission.apogee - mission.threat_tolerance_km
    # Perigee upper and lower bounds check data
    mission_perigee_upper_tol = mission.perigee + mission.threat_tolerance_km
    mission_perigee_lower_tol = mission.perigee - mission.threat_tolerance_km

    if mission_apogee_upper_tol > debris_apogee > mission_apogee_lower_tol:
        return True

    if mission_perigee_upper_tol > debris_perigee > mission_perigee_lower_tol:
        return True

    return False
