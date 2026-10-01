"""Card content for the '.NET Interview – Top 100' deck.

Each card is a dict with keys: id, tags, q, a, why, ex, src.
Field text uses a tiny markup: `inline code`, **bold**, and ``` fenced code blocks.
"""
from .runtime import CARDS as RUNTIME
from .csharp import CARDS as CSHARP
from .async_web import CARDS as ASYNC_WEB
from .data_arch import CARDS as DATA_ARCH

ALL_CARDS = RUNTIME + CSHARP + ASYNC_WEB + DATA_ARCH
