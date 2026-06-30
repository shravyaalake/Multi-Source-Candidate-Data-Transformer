from typing import Any


class OutputValidator:
    """
    Validates projected output against the runtime configuration.
    """

    TYPE_MAP = {
        "string": str,
        "number": (int, float),
        "boolean": bool,
        "string[]": list,
        "object": dict,
        "object[]": list,
    }

    # -----------------------------------------------------

    def validate(self, output: dict, config: dict):

        errors = []

        fields = config.get("fields", [])

        for field in fields:

            field_name = field["path"]

            required = field.get("required", False)

            expected_type = field.get("type")

            value = output.get(field_name)

            # ---------------------------------------
            # Required Validation
            # ---------------------------------------

            if required:

                if field_name not in output or value is None:

                    errors.append(
                        f"Required field missing: {field_name}"
                    )

                    continue

            # ---------------------------------------
            # Missing Field Handling
            # ---------------------------------------

            if value is None:
                continue

            # ---------------------------------------
            # Type Validation
            # ---------------------------------------

            if expected_type:

                python_type = self.TYPE_MAP.get(expected_type)

                if python_type is None:

                    errors.append(
                        f"Unknown type '{expected_type}' "
                        f"for field '{field_name}'"
                    )

                    continue

                if not isinstance(value, python_type):

                    errors.append(
                        f"Field '{field_name}' "
                        f"should be {expected_type}"
                    )

        return errors

    # -----------------------------------------------------

    def validate_or_raise(self, output, config):

        errors = self.validate(output, config)

        if errors:

            raise ValueError(

                "\n".join(errors)

            )

        return True