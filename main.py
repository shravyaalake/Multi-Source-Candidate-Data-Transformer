from src.parsers.csv_parser import CSVParser
from src.parsers.ats_parser import ATSParser
from src.parsers.resume_parser import ResumeParser
from src.merger.merger import CandidateMerger
from src.projection.projector import ProjectionEngine
csv_parser = CSVParser()
ats_parser = ATSParser()
resume_parser = ResumeParser()

csv_profiles = csv_parser.parse("input/recruiter.csv")
ats_profile = ats_parser.parse("input/ats.json")
resume_profile = resume_parser.parse("input/resume.pdf")

profiles = csv_profiles + [ats_profile, resume_profile]

merger = CandidateMerger()

candidate = merger.merge(profiles)

projector = ProjectionEngine()

config = projector.load_config("config/default.json")

output = projector.project(candidate, config)

import json

print(
    json.dumps(
        output,
        indent=4
    )
)