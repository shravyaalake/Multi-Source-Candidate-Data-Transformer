import json

from src.models.candidate import (
    CandidateProfile,
    Experience,
    Location,
    Provenance,
)


class ATSParser:
    """
    Parses candidate information from an ATS JSON export
    into the canonical CandidateProfile.
    """

    SOURCE = "ATS JSON"

    def parse(self, json_path: str) -> CandidateProfile:

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        candidate = CandidateProfile()

        # -------------------------
        # Basic Information
        # -------------------------

        candidate.full_name = data.get("candidateName")

        if data.get("mail"):
            candidate.emails.append(data["mail"])

        if data.get("mobile"):
            candidate.phones.append(data["mobile"])

        # -------------------------
        # Location
        # -------------------------

        candidate.location = Location(
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
        )

        # -------------------------
        # Experience
        # -------------------------

        if data.get("company") or data.get("designation"):

            candidate.experience.append(
                Experience(
                    company=data.get("company"),
                    title=data.get("designation"),
                    start=data.get("start_date"),
                    end=data.get("end_date"),
                    summary=data.get("summary"),
                )
            )

        # -------------------------
        # Headline
        # -------------------------

        candidate.headline = data.get("designation")

        # -------------------------
        # Confidence
        # -------------------------

        candidate.overall_confidence = 0.90

        # -------------------------
        # Provenance
        # -------------------------

        provenance_fields = [
            "full_name",
            "emails",
            "phones",
            "location",
            "experience",
            "headline",
        ]

        for field in provenance_fields:
            candidate.provenance.append(
                Provenance(
                    field=field,
                    source=self.SOURCE,
                    method="Field Mapping",
                )
            )

        return candidate