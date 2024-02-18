from orbital_debris_analysis.csv_parser.csv_parser import csv_to_pandas
from orbital_debris_analysis.debris_analysis.debris_analysis import extract_analysis_data, calculate_threat_model
from orbital_debris_analysis.models.mission import Mission


def test_extraction_of_debris_data():
    debris_data_frame = csv_to_pandas("./tests/data/SATCAT.csv")
    extracted_data = extract_analysis_data(debris_data_frame)
    assert extracted_data is not None


def test_debris_analysis():
    debris_data_frame = csv_to_pandas("./tests/data/SATCAT.csv")
    extracted_data = extract_analysis_data(debris_data_frame)
    threat_report = calculate_threat_model(data_frame=extracted_data, mission=Mission(apogee=700,
                                                                                      perigee=700,
                                                                                      threat_tolerance_km=100))
    print(threat_report)
    assert threat_report is not None
