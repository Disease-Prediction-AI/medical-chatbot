# from typing import Optional, List, Mapping, Any
# from langchain.llms.base import LLM
# from langchain.prompts import PromptTemplate
# import openai
# from langchain.chains import LLMChain
# import g4f
# from typing import List, Optional, Any
# from pydantic import BaseModel
# from langchain_core.language_models.chat_models import BaseMessage, CallbackManagerForLLMRun
# from functools import partial
# import asyncio



# class Message(BaseModel):
#     role: str
#     content: str

# class Conversation(BaseModel):
#     conversation: List[Message]

# class EducationalLLM:

#     @property
#     def _llm_type(self) -> str:
#         return "custom"

#     def __call__(
#         self,
#         messages: List[BaseMessage],
#         stop: Optional[List[str]] = None,
#         run_manager: Optional[CallbackManagerForLLMRun] = None,
#         **kwargs: Any,
#     ) -> str:    

#         out = g4f.ChatCompletion.create(
#             model=g4f.models.default,
#             messages=list(map(lambda message: {"role": message.type, "content": message.content}, messages)),
#         )
#         if stop:
#             stop_indexes = (out.find(s) for s in stop if s in out)
#             min_stop = min(stop_indexes, default=-1)
#             if min_stop > -1:
#                 out = out[:min_stop]
#         # out=HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature":0, "max_length":512})
#         return out
from typing import Optional, List, Any
from langchain_community.llms import HuggingFaceHub
from langchain.llms.base import LLM
from langchain_core.language_models.chat_models import BaseMessage, CallbackManagerForLLMRun
import os



class Message(BaseMessage):
    role: str
    content: str

class EducationalLLM:

    # def __init__(self):
    #     super().__init__()
        
    # @property
    # def _llm_type(self) -> str:
    #     return "custom"

    def __call__(
        self,
        messages: List[Message],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        hub = HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"temperature": 0.7, "max_length": 512})

        # Extract content from messages
        prompt_list = [f"{message.type}: {message.content}" for message in messages]

        # Generate responses for each prompt
        response = hub(prompt=''.join(prompt_list))
        

        if stop:
            stop_indexes = (response.find(s) for s in stop if s in response)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                response = response[:min_stop]

        return response

# Example usage:
# educational_llm = EducationalLLM()
# messages = [Message(role="user", content="Hello"), Message(role="assistant", content="Hi!")]
# output = educational_llm(messages=messages)
# print(output)
