import pandas as pd

from src.models.candidate import (
    CandidateProfile,
    Experience,
    Location,
    Provenance,
)


class CSVParser:
    """
    Parse Recruiter CSV into canonical CandidateProfile objects.
    """

    SOURCE = "Recruiter CSV"
    def safe_value(self, value):
        """
        Convert NaN values to None.
        """
        if pd.isna(value):
            return None
        return value
        
    def parse(self, csv_path: str):

        df = pd.read_csv(csv_path)

        candidates = []

        for _, row in df.iterrows():

            candidate = CandidateProfile()

            # ----------------------------------
            # Basic Information
            # ----------------------------------

            candidate.full_name = self.safe_value(row.get("name"))

            if pd.notna(row.get("email")):
                candidate.emails.append(str(row.get("email")))

            if pd.notna(row.get("phone")):
                candidate.phones.append(str(row.get("phone")))

            # ----------------------------------
            # Optional Location
            # ----------------------------------

            if (
                "city" in row
                or "region" in row
                or "country" in row
            ):

                candidate.location = Location(
                    city=self.safe_value(row.get("city")),
                    region=self.safe_value(row.get("region")),
                    country=self.safe_value(row.get("country")),
                )

            # ----------------------------------
            # Experience
            # ----------------------------------

            candidate.experience.append(

            Experience(
                company=self.safe_value(row.get("current_company")),
                title=self.safe_value(row.get("title")),
                start=self.safe_value(row.get("start_date")),
                end=self.safe_value(row.get("end_date")),
                summary=self.safe_value(row.get("summary")),
            )

            )

            # ----------------------------------
            # Headline
            # ----------------------------------

            candidate.headline = self.safe_value(row.get("title"))

            # ----------------------------------
            # Confidence
            # ----------------------------------

            candidate.overall_confidence = 0.95

            # ----------------------------------
            # Provenance
            # ----------------------------------

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

                        method="Exact Match",

                    )

                )

            candidates.append(candidate)

        return candidates

