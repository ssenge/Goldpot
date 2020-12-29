from dataclasses import dataclass, asdict
from typing import Iterable

import openai
from openai.openai_object import OpenAIObject

from goldpot.Config import DefaultConfig, CompletionConfig, Engine
from goldpot.Model import CompletionInput, CompletionOutput, SearchInput, SearchOutput


@dataclass
class Goldpot:
    api_key: str
    engine: Engine = DefaultConfig.engine
    max_chars: int = DefaultConfig.max_chars
    completion_config: CompletionConfig = DefaultConfig.completion_config

    def __post_init__(self):
        openai.api_key = self.api_key

    def complete_(self, prompt: str) -> OpenAIObject:
        return openai.Completion.create(engine=str(self.engine), prompt=prompt, **asdict(self.completion_config))

    def complete(self, input: CompletionInput) -> CompletionOutput:
        prompts = input.get_prompts()
        return CompletionOutput([self.complete_(prompt) for prompt in prompts], prompts)

    def search_(self, query: str, docs: Iterable[str]) -> OpenAIObject:
        return openai.Engine(str(self.engine)).search(documents=docs, query=query)

    def search(self, input: SearchInput) -> SearchOutput:
        return SearchOutput(
            [self.search_(q := query_docs[0], ds := query_docs[1]) for query_docs in input.get_docs()], input.docs)
