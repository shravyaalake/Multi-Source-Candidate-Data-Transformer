import argparse
import json

from src.parsers.csv_parser import CSVParser
from src.parsers.ats_parser import ATSParser
from src.parsers.resume_parser import ResumeParser
from src.merger.merger import CandidateMerger
from src.projection.projector import ProjectionEngine
from src.validation.validator import OutputValidator


def main():

    parser = argparse.ArgumentParser(
        description="Multi-Source Candidate Data Transformer"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Recruiter CSV input file"
    )

    parser.add_argument(
        "--ats",
        required=True,
        help="ATS JSON input file"
    )

    parser.add_argument(
        "--resume",
        required=True,
        help="Resume PDF input file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Projection configuration JSON"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file"
    )

    args = parser.parse_args()

    # -------------------------------
    # Parse inputs
    # -------------------------------

    csv_profiles = CSVParser().parse(args.csv)

    ats_profile = ATSParser().parse(args.ats)

    resume_profile = ResumeParser().parse(args.resume)

    profiles = csv_profiles + [ats_profile, resume_profile]

    # -------------------------------
    # Merge
    # -------------------------------

    candidate = CandidateMerger().merge(profiles)

    # -------------------------------
    # Projection
    # -------------------------------

    projector = ProjectionEngine()

    config = projector.load_config(args.config)

    output = projector.project(candidate, config)

    # -------------------------------
    # Validation
    # -------------------------------

    OutputValidator().validate_or_raise(
        output,
        config
    )

    # -------------------------------
    # Save output
    # -------------------------------

    if args.output:

        with open(args.output, "w", encoding="utf-8") as f:

            json.dump(
                output,
                f,
                indent=4
            )

    # -------------------------------
    # Print output
    # -------------------------------

    print(
        json.dumps(
            output,
            indent=4
        )
    )


if __name__ == "__main__":
    main()