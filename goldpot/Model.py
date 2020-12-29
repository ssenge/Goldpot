import re
from dataclasses import dataclass, field
from typing import Optional, Iterable, Any, Dict, Tuple

from openai.openai_object import OpenAIObject

from goldpot import DefaultConfig
from goldpot.Utils import Splitter


@dataclass
class CompletionInput:
    start: str = ''
    end: str = ''
    max_chars: int = DefaultConfig.max_chars
    sep: str = '\n'
    sample_sep: str = '----'
    samples: Iterable[str] = field(default_factory=lambda: [])

    def get_prompts(self):
        samples = ''.join([self.sep + sample + self.sep + self.sample_sep + self.sep for sample in self.samples])
        begin = (self.start + samples)[:self.max_chars]
        left_chars = self.max_chars - len(begin)
        splits = Splitter.len_chunk_split(re.findall('[\w\W]*?[.!?]|[\w\W]+', self.end), left_chars)
        return [begin + ''.join(s) for split in splits for s in split]


@dataclass
class SearchInput:
    query: str
    docs: [str]
    max_chars: int = DefaultConfig.max_chars

    def get_docs(self):
        left_chars = self.max_chars - len(self.query)
        docs_split = Splitter.len_chunk_split(self.docs, left_chars)
        return [(self.query, d) for docs in docs_split for d in docs]


@dataclass
class CompletionResult:
    prompt: str
    finish_reason: str
    text: str
    logprobs: Any


@dataclass
class CompletionOutput:
    output: Iterable[OpenAIObject]
    prompts: Iterable[str]
    completion: str = ''
    completions: Iterable[str] = field(default_factory=lambda: [])
    results: Iterable[CompletionResult] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.results = [CompletionResult(oo[1], c.finish_reason, c.text, c.logprobs) for oo in
                        zip(self.output, self.prompts) for c in oo[0].choices]
        self.completions = [r.text for r in self.results]
        self.completion = '\n'.join(self.completions)


@dataclass
class SearchOutput:
    output: Iterable[OpenAIObject]
    docs: Iterable
    scores: Dict[str, float] = field(default_factory=lambda: {})
    scores_sorted: Iterable[Tuple[str, float]] = field(default_factory=lambda: [])

    def __post_init__(self):
        clip = lambda f: max(min(300.0, f), 0.0) / 300.0
        r = [(o.score, clip(o.score)) for oo in self.output for o in oo.data]
        self.scores = dict(zip(self.docs, r))
        self.scores_sorted = sorted(self.scores.items(), key=lambda i: i[1][1], reverse=True)