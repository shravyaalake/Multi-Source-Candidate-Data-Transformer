from src.parsers.csv_parser import CSVParser

parser = CSVParser()

profiles = parser.parse("input/recruiter.csv")

for p in profiles:
    print(p.model_dump_json(indent=4))