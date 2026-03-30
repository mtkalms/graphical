from typing import Literal

Orientation = Literal[
    "horizontal",
    "vertical",
]
OptimizationStrategy = Literal[
    "never",
    "full",
    "all",
]
InversionStrategy = Literal[
    "reverse",  # Use reverse ANSI code
    "swap",  # Swap color and bgcolor
]
