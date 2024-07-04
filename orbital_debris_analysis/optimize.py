import httpx
import asyncio
import csv
from pydantic import BaseModel


class Mission(BaseModel):
    apogee: int
    perigee: int
    threat_tolerance_km: int


class ThreatReport(BaseModel):
    total_threat_count: int
    rocket_body_threat_count: int
    debris_threat_count: int
    inactive_sat_threat_count: int
    active_sat_threat_count: int


async def send_mission_data(apogee_perigee: int, threat_tolerance_km: int) -> ThreatReport:
    url = 'http://localhost:8080/api/threat-report/'
    mission = Mission(apogee=apogee_perigee, perigee=apogee_perigee, threat_tolerance_km=threat_tolerance_km)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=mission.dict(), timeout=500000)
        response.raise_for_status()
        threat_report = ThreatReport(**response.json())
        return threat_report


async def main():
    start_altitude = 1681
    end_altitude = 1681
    step_size = 5
    threat_tolerance_km = 0

    # Open the CSV file for writing
    with open("mission_all_threats.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Altitude', 'Total Threat Count'])

        # Iterate over the altitude range
        for tolerance in range(0, 10 + 1, 1):
            threat_report = await send_mission_data(apogee_perigee=start_altitude, threat_tolerance_km=tolerance)
            # Write each altitude and its total threat count to the CSV
            writer.writerow([tolerance, threat_report.total_threat_count, threat_report.rocket_body_threat_count, threat_report.debris_threat_count, threat_report.active_sat_threat_count, threat_report.inactive_sat_threat_count])
            print(f"tolerance: {tolerance}km, Total Threat Count: {threat_report.total_threat_count}")



def opt():
    asyncio.run(main())