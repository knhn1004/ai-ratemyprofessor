import json
import logging
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ai_rmp_api.handler import TokenByTokenHandler
from ai_rmp_api.tools import tools
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq


import logging
from fastapi.encoders import jsonable_encoder

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


llm = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, return_intermediate_steps=True
)


class Query(BaseModel):
    input: str


@app.post("/stream")
async def stream_response(query: Query):
    async def event_generator():
        handler = TokenByTokenHandler(tags_of_interest=["tool_llm", "agent_llm"])
        try:
            async for event in agent_executor.astream_events(
                {"input": query.input},
                version="v1",
                config={"callbacks": [handler]},
            ):
                kind = event["event"]
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield f"data: {json.dumps({'content': content})}\n\n"
                elif kind in [
                    "on_llm_start",
                    "on_llm_end",
                    "on_chain_start",
                    "on_chain_end",
                    "on_tool_start",
                    "on_tool_end",
                ]:
                    # Serialize the event data
                    serialized_data = jsonable_encoder(event["data"])
                    yield f"data: {json.dumps({'event': kind, 'data': serialized_data})}\n\n"
        except Exception as e:
            logger.error(f"Error in event_generator: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


def start():
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
