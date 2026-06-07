from typing import Any


def assert_greater_or_equal(
    actual_value: Any,
    expected_value: Any,
    error_msg: str | None = None,
) -> None:
    if actual_value < expected_value:
        raise AssertionError(
            error_msg
            or (
                "Value is less than expected: "
                f"actual={actual_value}, expected={expected_value}"
            )
        )
