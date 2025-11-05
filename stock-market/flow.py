# Bring in dependencies
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from colorama import Fore
from dotenv import load_dotenv

from langgraph.prebuilt import ToolNode
from tool import simple_screener

load_dotenv()

# Create LLM
llm = AzureChatOpenAI(azure_deployment="gpt-4o")

# Create tool
tools = [simple_screener]

# Bind the llm with tools
llm_with_tools = llm.bind_tools(tools)

# Create tool node
tool_node = ToolNode(tools)

# Create State
class State(dict):
    messages: Annotated[list, add_messages]


# Build llm node
def chatbot(state: State):
    # Get LLM response
    response = llm_with_tools.invoke(state["messages"])
    # Return response in correct message format
    return {"messages": [response]}


# Create router node
def router(state: State):
    last_message = state['messages'][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return END

# Assemble a graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_conditional_edges("chatbot", router)

# graph_builder.add_edge("chatbot", END)

# Add memory and compile graph
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)




# Build call loop and run it
if __name__ == "__main__":
    while True:
        prompt = input("\n🤖Input your prompt:")
        res = graph.invoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config={"configurable": {"thread_id": 1234}},
        )
        print(Fore.LIGHTYELLOW_EX + res["messages"][-1].content + Fore.RESET)
