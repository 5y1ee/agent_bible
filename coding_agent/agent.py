from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools import python_exec_tool, file_write_tool

load_dotenv()

tools = [python_exec_tool, file_write_tool]

llm = ChatOpenAI(model_name="gpt-4o")
graph = create_agent(llm, tools)

if __name__ == "__main__":
    response = graph.stream(
        {
            "messages": [
                "첫 번째 항이 1인 피보나치 수열을 출력하는 파이썬 코드를 작성하고, "
                "반드시 python_exec_tool 도구를 호출해서 실행까지 해줘.",
                "확인했다면 그 코드는 .py 파일로 저장해줘"
            ]
        }
    )
    for chunk in response: 
        for node, value in chunk.items(): 
            if node: 
                print("---", node, "---") 
            if "messages" in value: 
                print(value['messages'][0].content)