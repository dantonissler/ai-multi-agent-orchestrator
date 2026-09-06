from typing import NotRequired

from typing_extensions import TypedDict


class LegalState(TypedDict):
    publication_text: str
    is_favorable: NotRequired[bool]
    analysis_reason: NotRequired[str]
    drafted_appeal: NotRequired[str]
    protocol_receipt: NotRequired[str]
