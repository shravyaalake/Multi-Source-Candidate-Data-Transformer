import phonenumbers


class PhoneNormalizer:

    @staticmethod
    def normalize(phone):

        if phone is None:
            return None

        phone = str(phone).strip()

        try:

            parsed = phonenumbers.parse(phone, "IN")

            if phonenumbers.is_valid_number(parsed):

                return phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164
                )

        except Exception:

            return None

        return None