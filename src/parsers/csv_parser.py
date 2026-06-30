import pandas as pd
import uuid

from src.models.candidate import (
    CandidateProfile,
    Experience,
    Provenance
)


class CSVParser:

    def parse(self, csv_path):

        df = pd.read_csv(csv_path)

        candidates = []

        for _, row in df.iterrows():

            candidate = CandidateProfile(

                candidate_id=str(uuid.uuid4()),

                full_name=row.get("name"),

                emails=[row.get("email")],

                phones=[str(row.get("phone"))],

                experience=[
                    Experience(
                        company=row.get("current_company"),
                        title=row.get("title")
                    )
                ],

                provenance=[

                    Provenance(
                        field="full_name",
                        source="Recruiter CSV",
                        method="Exact Match"
                    ),

                    Provenance(
                        field="email",
                        source="Recruiter CSV",
                        method="Exact Match"
                    ),

                    Provenance(
                        field="phone",
                        source="Recruiter CSV",
                        method="Exact Match"
                    )

                ],

                overall_confidence=0.95

            )

            candidates.append(candidate)

        return candidates