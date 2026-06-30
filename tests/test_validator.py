from src.validation.validator import OutputValidator


def test_validator():

    output = {

        "name":"Shravya"

    }

    config = {

        "fields":[

            {

                "path":"name",

                "required":True,

                "type":"string"

            }

        ]

    }

    validator = OutputValidator()

    assert validator.validate(output, config) == []