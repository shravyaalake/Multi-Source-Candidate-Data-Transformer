import json
from typing import Any

from pydantic import BaseModel


class ProjectionEngine:

    def load_config(self, config_path: str):

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ----------------------------------------------------

    def serialize(self, value):
        """
        Convert Pydantic models into plain Python objects.
        """

        if isinstance(value, BaseModel):
            return value.model_dump()

        if isinstance(value, list):

            serialized = []

            for item in value:

                if isinstance(item, BaseModel):
                    serialized.append(item.model_dump())
                else:
                    serialized.append(item)

            return serialized

        return value

    # ----------------------------------------------------

    def get_value(self, obj: Any, path: str):

        if path is None:
            return None

        # skills[].name

        if "[]" in path:

            collection, field = path.split("[].")

            items = getattr(obj, collection, [])

            return [
                getattr(item, field, None)
                for item in items
            ]

        # emails[0]

        if "[" in path:

            field = path[:path.index("[")]

            index = int(
                path[path.index("[") + 1:path.index("]")]
            )

            values = getattr(obj, field, [])

            if index < len(values):
                return values[index]

            return None

        # location.city (nested object)

        if "." in path:

            current = obj

            for part in path.split("."):

                if current is None:
                    return None

                current = getattr(current, part, None)

            return current

        # simple field

        return getattr(obj, path, None)

    # ----------------------------------------------------

    def project(self, candidate, config):

        output = {}

        on_missing = config.get("on_missing", "null")

        for field in config["fields"]:

            output_key = field["path"]

            source = field.get("from", output_key)

            value = self.get_value(candidate, source)

            value = self.serialize(value)

            if value is None:

                if on_missing == "omit":
                    continue

                if on_missing == "error":
                    raise ValueError(
                        f"Missing required field: {source}"
                    )

                output[output_key] = None

            else:

                output[output_key] = value

        if config.get("include_confidence", False):

            output["overall_confidence"] = candidate.overall_confidence

        if config.get("include_provenance", False):

            output["provenance"] = [

                p.model_dump()

                for p in candidate.provenance

            ]

        return output