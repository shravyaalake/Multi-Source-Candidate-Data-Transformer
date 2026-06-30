from src.projection.projector import ProjectionEngine
from src.models.candidate import CandidateProfile


def test_projection():

    candidate = CandidateProfile(
        full_name="Shravya Alake",
        emails=["abc@gmail.com"]
    )

    config = {
        "fields":[
            {
                "path":"candidate_name",
                "from":"full_name"
            }
        ]
    }

    output = ProjectionEngine().project(candidate, config)

    assert output["candidate_name"] == "Shravya Alake"