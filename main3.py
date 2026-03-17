from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv

load_dotenv()

tool = TavilySearch(max_results=3, api_key=os.getenv("TAVILY_API_KEY"))
tools = [tool]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

###

from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


###


def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


graph_builder.add_node("chatbot", chatbot)

###

import json
from langchain.messages import ToolMessage


class BasicToolNode:
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("ERROR: 입력에 메시지가 없습니다.")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=False),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}


tool_node = BasicToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)


def route_tools(state: State):
    """마지막 메시지에 도구 호출이 있는 경우, ToolNode로 라우팅하고 그렇지 않으면 END로 라우팅"""
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"ERROR: 입력에 메시지가 없습니다. 상태: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)

graph_builder.add_edge("tools", "chatbot") 
graph_builder.add_edge(START, "chatbot") 
graph = graph_builder.compile()

if __name__ == "__main__":
    try:
        image = graph.get_graph().draw_mermaid_png()
        os.makedirs("web_agent", exist_ok=True)
        with open("web_agent/graph.png", "wb") as f:
            f.write(image)
        print("graph image saved: web_agent/graph.png")
    except Exception as e:
        print(f"graph image save failed: {e}")

    response = graph.invoke({"messages": ["Langgraph가 무엇인가요?"]})
    print(response)
