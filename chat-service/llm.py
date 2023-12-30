from typing import Optional, List, Mapping, Any
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
import openai
from langchain.chains import LLMChain
import g4f
from typing import List, Optional, Any
from pydantic import BaseModel
from langchain_core.language_models.chat_models import BaseMessage, CallbackManagerForLLMRun
from functools import partial
import asyncio



class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

class EducationalLLM:

    @property
    def _llm_type(self) -> str:
        return "custom"

    def __call__(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:    

        out = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=list(map(lambda message: {"role": message.type, "content": message.content}, messages)),
        )  #
        if stop:
            stop_indexes = (out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        
        return out