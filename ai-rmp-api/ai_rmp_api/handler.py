from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from langchain.callbacks.base import AsyncCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult


class TokenByTokenHandler(AsyncCallbackHandler):
    def __init__(self, tags_of_interest: List[str]) -> None:
        """A custom call back handler.

        Args:
            tags_of_interest: Only LLM tokens from models with these tags will be
                              printed.
        """
        self.tags_of_interest = tags_of_interest

    async def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain starts running."""
        print("on chain start: ")
        print(inputs)

    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain ends running."""
        print("On chain end")
        print(outputs)

    async def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when a chat model starts running."""
        overlap_tags = self.get_overlap_tags(tags)

        if overlap_tags:
            print(",".join(overlap_tags), end=": ", flush=True)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool starts running."""
        print("Tool start")
        print(serialized)

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool ends running."""
        print("Tool end")
        print(str(output))

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM ends running."""
        overlap_tags = self.get_overlap_tags(tags)

        if overlap_tags:
            # Who can argue with beauty?
            print()
            print()

    def get_overlap_tags(self, tags: Optional[List[str]]) -> List[str]:
        """Check for overlap with filtered tags."""
        if not tags:
            return []
        return sorted(set(tags or []) & set(self.tags_of_interest or []))

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        overlap_tags = self.get_overlap_tags(tags)

        if token and overlap_tags:
            print(token, end="|", flush=True)
