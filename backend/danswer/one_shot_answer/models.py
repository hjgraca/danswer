from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator

from danswer.chat.models import DanswerContexts
from danswer.chat.models import DanswerQuotes
from danswer.chat.models import QADocsResponse
from danswer.configs.constants import MessageType
from danswer.search.models import RetrievalDetails


class QueryRephrase(BaseModel):
    rephrased_query: str


class ThreadMessage(BaseModel):
    message: str
    sender: str | None
    role: MessageType = MessageType.USER


class DirectQARequest(BaseModel):
    messages: list[ThreadMessage]
    prompt_id: int | None
    persona_id: int
    retrieval_options: RetrievalDetails = Field(default_factory=RetrievalDetails)
    chain_of_thought: bool = False
    return_contexts: bool = False

    @root_validator
    def check_chain_of_thought_and_prompt_id(
        cls, values: dict[str, Any]
    ) -> dict[str, Any]:
        chain_of_thought = values.get("chain_of_thought")
        prompt_id = values.get("prompt_id")

        if chain_of_thought and prompt_id is not None:
            raise ValueError(
                "If chain_of_thought is True, prompt_id must be None"
                "The chain of thought prompt is only for question "
                "answering and does not accept customizing."
            )

        return values


class OneShotQAResponse(BaseModel):
    # This is built piece by piece, any of these can be None as the flow could break
    answer: str | None = None
    rephrase: str | None = None
    quotes: DanswerQuotes | None = None
    docs: QADocsResponse | None = None
    llm_chunks_indices: list[int] | None = None
    error_msg: str | None = None
    answer_valid: bool = True  # Reflexion result, default True if Reflexion not run
    chat_message_id: int | None = None
    contexts: DanswerContexts | None = None
