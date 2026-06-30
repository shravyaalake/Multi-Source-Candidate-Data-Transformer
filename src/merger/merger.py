from copy import deepcopy

from src.models.candidate import CandidateProfile
from src.normalizer.phone import PhoneNormalizer


class CandidateMerger:

    def merge(self, profiles: list[CandidateProfile]) -> CandidateProfile:
        """
        Merge multiple candidate profiles into one canonical profile.
        """

        if not profiles:
            raise ValueError("No candidate profiles provided.")

        # Highest confidence profile becomes the base profile
        profiles = sorted(
            profiles,
            key=lambda p: p.overall_confidence,
            reverse=True
        )

        merged = deepcopy(profiles[0])

        for profile in profiles[1:]:

            self.merge_name(merged, profile)

            self.merge_emails(merged, profile)

            self.merge_phones(merged, profile)

            self.merge_location(merged, profile)

            self.merge_experience(merged, profile)

            self.merge_education(merged, profile)

            self.merge_skills(merged, profile)

            self.merge_provenance(merged, profile)

            merged.overall_confidence = max(
                merged.overall_confidence,
                profile.overall_confidence
            )

        return merged

    # -------------------------------------------------------

    def merge_name(self, merged, profile):

        if profile.full_name:

            if (
                merged.full_name is None
                or len(profile.full_name) > len(merged.full_name)
            ):

                merged.full_name = profile.full_name

    # -------------------------------------------------------

    def merge_emails(self, merged, profile):

        merged.emails = list(
            dict.fromkeys(
                merged.emails + profile.emails
            )
        )

    # -------------------------------------------------------

    def merge_phones(self, merged, profile):

        phones = []

        for phone in merged.phones + profile.phones:

            normalized = PhoneNormalizer.normalize(phone)

            if normalized:
                phones.append(normalized)

        merged.phones = list(dict.fromkeys(phones))

    # -------------------------------------------------------

    def merge_location(self, merged, profile):

        if merged.location is None:

            merged.location = profile.location

            return

        if profile.location is None:
            return

        if not merged.location.city:
            merged.location.city = profile.location.city

        if not merged.location.region:
            merged.location.region = profile.location.region

        if not merged.location.country:
            merged.location.country = profile.location.country

    # -------------------------------------------------------

    def merge_experience(self, merged, profile):

        existing = {

            (
                exp.company,
                exp.title,
                exp.start,
                exp.end
            )

            for exp in merged.experience
        }

        for exp in profile.experience:

            key = (

                exp.company,
                exp.title,
                exp.start,
                exp.end

            )

            if key not in existing:

                merged.experience.append(exp)

                existing.add(key)

    # -------------------------------------------------------

    def merge_education(self, merged, profile):

        existing = {

            (
                edu.institution,
                edu.degree,
                edu.end_year
            )

            for edu in merged.education
        }

        for edu in profile.education:

            key = (

                edu.institution,
                edu.degree,
                edu.end_year

            )

            if key not in existing:

                merged.education.append(edu)

                existing.add(key)

    # -------------------------------------------------------

    def merge_skills(self, merged, profile):

        existing = {

            skill.name.lower()

            for skill in merged.skills
        }

        for skill in profile.skills:

            if skill.name.lower() not in existing:

                merged.skills.append(skill)

                existing.add(skill.name.lower())

    # -------------------------------------------------------

    def merge_provenance(self, merged, profile):

        merged.provenance.extend(profile.provenance)