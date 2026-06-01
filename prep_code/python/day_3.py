from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: int
    customer_id: int
    amount: float


from pydantic import ValidationError

from nova.models.pydantic_models import Transaction


def validate_transactions(records: list[dict]):
    """
    Validate transaction records using Pydantic.

    Returns:
        tuple[list, list]
        (
            valid_records,
            invalid_records
        )
    """

    valid_records = []
    invalid_records = []

    for record in records:
        try:
            validated_record = Transaction(**record)

            valid_records.append(
                validated_record.model_dump()
            )

        except ValidationError as e:
            invalid_records.append(
                {
                    "record": record,
                    "errors": e.errors()
                }
            )

    return valid_records, invalid_records