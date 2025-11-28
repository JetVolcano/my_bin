import math
import string
import sys
from typing import Final


class Binary:
    """
    How it works
    ------------

    The integer system is the same as normal but instead of floating point numbers
    we take the binary representation of the number after the decimal point
    and convert that to a decimal and then put the decimal behind the decimal point.

    For Example:
    ------------

    **8 4 2 1 | 8 4 2 1 | 1 2 4 8**

    **0 1 1 1 | 0 0 0 1 | 1 0 1 0**
    **7.05**

    When you reverse the binary number behind the | you get 0101 then convert that into decimal,
    you get 5. so the number behind the decimal point is 5.
    The number you get before the | is 7. Finally, the middle section is for the amount of zeros
    before  the decimal. So 111.1.101 is 7.05
    """

    def __init__(
        self,
        precision: int = math.log2(sys.maxsize + 1).__int__(),
        show_postives: bool = False,
    ) -> None:
        self.__ERRORS: Final[tuple[ValueError, TypeError]] = (
            ValueError(
                f"Invalid Precision: {precision}. Precision must be greater than 0"
            ),
            TypeError(f"Precision must be an integer, not {type(precision)}"),
        )
        if precision < 1:
            raise self.__ERRORS[0]
        if not isinstance(precision, int):
            raise self.__ERRORS[1]
        self.__precision: int = precision
        self.postives: bool = show_postives

    @property
    def precision(self) -> int:
        return self.__precision

    @precision.setter
    def precision(self, value: int) -> None:
        if value < 1:
            raise self.__ERRORS[0]
        if not isinstance(value, int):
            raise self.__ERRORS[1]
        self.__precision = value

    def encode(self, number: str, postive: bool = True) -> str:
        SPLIT: Final[list[str]] = number.split(".")
        SPLIT_LEN: Final[int] = len(SPLIT)
        DECIMAL_COUNT: Final[int] = number.count(".")
        DECIMAL_COUNT_MAX: Final[int] = 1
        FRACTIONAL_REQUIREMENT: Final[int] = 2
        FRACTIONAL: Final[bool] = SPLIT_LEN == FRACTIONAL_REQUIREMENT
        VALID_CHARACTERS: Final[str] = f".{string.digits}"
        ALL_VALID: Final[bool] = all(
            character in VALID_CHARACTERS for character in number
        )
        ERRORS: Final[tuple[ValueError, ValueError]] = (
            ValueError(f"Too many decimal points: {DECIMAL_COUNT}. Amounts: 0 or 1"),
            ValueError(
                f"Invalid decimal number. Valid characters: {', '.join(VALID_CHARACTERS)}"
            ),
        )
        if DECIMAL_COUNT > DECIMAL_COUNT_MAX:
            raise ERRORS[0]
        if not ALL_VALID:
            raise ERRORS[1]
        whole: str = bin(int(SPLIT[0])).removeprefix("0b")
        fraction: str = ""
        zeros: int = 0
        if FRACTIONAL:
            for i in range(len(SPLIT[1])):
                if SPLIT[1][i] == "0":
                    zeros += 1
                else:
                    break
            fraction = f"{bin(int(SPLIT[1]))}".removeprefix("0b")
        postives_display: str = f"{'+' if self.postives else ''}"
        sign_display: str = f"{postives_display if postive else '-'}"
        zeros_part: str = f"{'.' if FRACTIONAL else ''}{bin(zeros).removeprefix('0b')}"
        fractional_part: str = f"{'.' if FRACTIONAL else ''}{fraction}"
        return f"{sign_display}{whole}{zeros_part}{fractional_part}"[: self.__precision]

    def decode(self, number: str, postive: bool = True) -> str:
        SPLIT: Final[list[str]] = number.split(".")
        SPLIT_LEN: Final[int] = len(SPLIT)
        DECIMAL_COUNT: Final[int] = number.count(".")
        DECIMAL_COUNT_MIN: Final[int] = 0
        DECIMAL_COUNT_MAX: Final[int] = 2
        FRACTIONAL_REQUIREMENT: Final[int] = 3
        FRACTIONAL: Final[bool] = SPLIT_LEN == FRACTIONAL_REQUIREMENT
        VALID_CHARACTERS: Final[str] = "01."
        ALL_VALID: Final[bool] = all(
            character in VALID_CHARACTERS for character in number
        )
        ERRORS: Final[tuple[ValueError, ValueError, ValueError]] = (
            ValueError(f"Too many decimal points: {DECIMAL_COUNT}. Amounts: 0 or 2"),
            ValueError(
                f"Too little decimal points: {DECIMAL_COUNT} for a fractional number. Amounts: 0 or 2"
            ),
            ValueError(
                f"Invalid Binary representation. Valid characters: {', '.join(VALID_CHARACTERS)}"
            ),
        )
        if DECIMAL_COUNT > DECIMAL_COUNT_MAX:
            raise ERRORS[0]
        if DECIMAL_COUNT_MIN < DECIMAL_COUNT < DECIMAL_COUNT_MAX:
            raise ERRORS[1]
        if not ALL_VALID:
            raise ERRORS[2]
        whole: str = f"{int(SPLIT[0], 2)}"
        fraction: str = ""
        zeros: int = 0
        if FRACTIONAL:
            zeros = int(SPLIT[1], 2)
            fraction = f".{'0' * zeros}{int(SPLIT[2], 2)}"
        postives_display: str = f"{'+' if self.postives else ''}"
        sign_display: str = f"{postives_display if postive else '-'}"
        return f"{sign_display}{whole}{fraction}"[: self.__precision]
