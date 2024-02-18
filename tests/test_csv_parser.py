from orbital_debris_analysis.csv_parser.csv_parser import csv_to_pandas


def test_csv_parser_can_parse():
    csv_to_pandas("./tests/data/SATCAT.csv")
