from langchain_groq import ChatGroq
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from dotenv import load_dotenv
from ai_rmp_api.tools import tools
from langchain.tools.human import HumanInputRun


def main():
    load_dotenv()

    llm = ChatGroq(
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = hub.pull("hwchase17/openai-tools-agent")

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=[*tools, HumanInputRun()], verbose=True
    )
    _input = input("Enter a query: ")
    agent_executor.invoke({"input": _input})
