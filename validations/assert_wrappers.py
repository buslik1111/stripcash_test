from typing import Any


def assert_greater(
    actual_value: Any,
    expected_value: Any,
    error_msg: str | None = None,
) -> None:
    if actual_value <= expected_value:
        raise AssertionError(
            error_msg
            or (
                "Value is not greater than expected: "
                f"actual={actual_value}, expected={expected_value}"
            )
        )
