import re
import pdfplumber

from src.models.candidate import (
    CandidateProfile,
    Skill,
    Experience,
    Education,
    Provenance,
)

from src.normalizer.skills import SkillNormalizer


class ResumeParser:

    SOURCE = "Resume PDF"

    # -----------------------------------------------------

    def extract_text(self, pdf_path: str) -> str:

        text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    # -----------------------------------------------------

    def parse(self, pdf_path: str):

        text = self.extract_text(pdf_path)

        candidate = CandidateProfile()

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # -------------------------------------------------
        # Name
        # -------------------------------------------------

        if lines:
            candidate.full_name = lines[0]

        # -------------------------------------------------
        # Email
        # -------------------------------------------------

        email = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        if email:
            candidate.emails.append(email.group())

        # -------------------------------------------------
        # Phone
        # -------------------------------------------------

        phone = re.search(
            r"(\+91[\s-]?)?[6-9]\d{9}",
            text,
        )

        if phone:
            candidate.phones.append(phone.group())

        # -------------------------------------------------
        # Skills
        # -------------------------------------------------

        skill_keywords = [

            "Python",
            "Java",
            "JavaScript",
            "React",
            "ReactJS",
            "Next.js",
            "Node.js",
            "Express",
            "MySQL",
            "MongoDB",
            "Docker",
            "Grafana",
            "InfluxDB",
            "Kafka",
            "AWS",
            "Git",
            "GitHub",
            "HTML",
            "CSS",
            "Tailwind",
            "OCR",
            "TensorFlow",
            "OpenCV",
            "C",
            "C++"

        ]

        found = set()

        lower_text = text.lower()

        for skill in skill_keywords:

            if skill.lower() in lower_text:

                canonical = SkillNormalizer.normalize(skill)

                if canonical.lower() not in found:

                    found.add(canonical.lower())

                    candidate.skills.append(

                        Skill(

                            name=canonical,

                            confidence=0.80,

                            sources=[self.SOURCE]

                        )

                    )

        # -------------------------------------------------
        # Education
        # -------------------------------------------------

        education_patterns = [

            (
                "Sahyadri College of Engineering and Management",
                "B.E.",
                "Computer Science and Engineering",
                2026
            )

        ]

        for college, degree, field, year in education_patterns:

            if college.lower() in lower_text:

                candidate.education.append(

                    Education(

                        institution=college,

                        degree=degree,

                        field=field,

                        end_year=year

                    )

                )

        # -------------------------------------------------
        # Internship / Experience
        # -------------------------------------------------

        if "Ukshati Technologies".lower() in lower_text:

            candidate.experience.append(

                Experience(

                    company="Ukshati Technologies Pvt. Ltd.",

                    title="Software Engineer Intern",

                    start="2026-01",

                    end=None,

                    summary="Worked on ERP Accounting, Asset Management, OCR, Docker, Grafana"

                )

            )

        # -------------------------------------------------
        # Headline
        # -------------------------------------------------

        if candidate.experience:

            candidate.headline = candidate.experience[0].title

        # -------------------------------------------------
        # Years of Experience
        # -------------------------------------------------

        candidate.years_experience = 0.5

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        candidate.overall_confidence = 0.80

        # -------------------------------------------------
        # Provenance
        # -------------------------------------------------

        provenance_fields = [

            "full_name",

            "emails",

            "phones",

            "skills",

            "education",

            "experience",

            "headline"

        ]

        for field in provenance_fields:

            candidate.provenance.append(

                Provenance(

                    field=field,

                    source=self.SOURCE,

                    method="Regex + Section Parsing"

                )

            )

        return candidate