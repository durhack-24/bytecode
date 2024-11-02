from enum import EnumType


class Duration(EnumType):
    sixteenth = 1
    eighth = 2
    quarter = 4
    half = 8
    whole = 16

    @staticmethod
    def parse_duration(duration: str) -> int:
        return {
            "sixteenth": Duration.sixteenth,
            "eighth": Duration.eighth,
            "quarter": Duration.quarter,
            "half": Duration.half,
            "whole": Duration.whole
        }[duration]
