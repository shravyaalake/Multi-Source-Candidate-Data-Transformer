from src.merger.merger import CandidateMerger
from src.models.candidate import CandidateProfile


def test_merge_name():

    c1 = CandidateProfile(
        full_name="Shravya"
    )

    c2 = CandidateProfile(
        full_name="Shravya Alake"
    )

    merged = CandidateMerger().merge([c1, c2])

    assert merged.full_name == "Shravya Alake"