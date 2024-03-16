from langchain_community.utilities import OpenWeatherMapAPIWrapper
from dotenv import load_dotenv
import os
from langgraph.graph import Graph
from langchain_openai import ChatOpenAI

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_community.tools.openweathermap import OpenWeatherMapQueryRun
from langchain_core.utils.function_calling import convert_to_openai_function
from langgraph.prebuilt import ToolInvocation
import json
from langchain_core.messages import FunctionMessage
from langgraph.prebuilt import ToolExecutor
#from agentstate import AgentState
from langgraph.graph import StateGraph, END

from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage


#TODO add .env
load_dotenv()
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv('OPENWEATHERMAP_API_KEY')
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"


def initialize_app():
    
    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], operator.add]


    def function_1(state):
        messages = state['messages']
        response = model.invoke(messages)
        return {"messages": [response]}


    def function_2(state):
        messages = state['messages']
        last_message = messages[-1] # this has the query we need to send to the tool provided by the agent

        parsed_tool_input = json.loads(last_message.additional_kwargs["function_call"]["arguments"])

        # We construct an ToolInvocation from the function_call and pass in the tool name and the expected str input for OpenWeatherMap tool
        action = ToolInvocation(
            tool=last_message.additional_kwargs["function_call"]["name"],
            tool_input=parsed_tool_input['__arg1'],
        )
        
        # We call the tool_executor and get back a response
        response = tool_executor.invoke(action)

        # We use the response to create a FunctionMessage
        function_message = FunctionMessage(content=str(response), name=action.tool)

        # We return a list, because this will get added to the existing list
        return {"messages": [function_message]}


    def where_to_go(state):
        messages = state['messages']
        last_message = messages[-1]
        
        if "function_call" in last_message.additional_kwargs:
            return "continue"
        else:
            return "end"

    tools = [OpenWeatherMapQueryRun()]

    model = ChatOpenAI(temperature=0, streaming=True)
    functions = [convert_to_openai_function(t) for t in tools]
    model = model.bind_functions(functions)

    tool_executor = ToolExecutor(tools)

    ##Graph setup

    workflow = StateGraph(AgentState)

    workflow.add_node('agent', function_1)
    workflow.add_node('tool', function_2)


    workflow.add_conditional_edges("agent",where_to_go,
                                {
                                "continue":"tool",
                                "end" : END
                                } # keys are smth that is returned from where_to_go, values are downnstream node to call if the condition is returned
    )
    
    #add normal edge from 'tools' to 'agent'. This edge is MUST, so that it is `tool` -> `agent ( see Blue and Red arrows on the figure) `
    workflow.add_edge('tool', 'agent')

    workflow.set_entry_point('agent')

    app = workflow.compile()

    return app, model


def process_input(user_input):
    inputs = {"messages": [HumanMessage(content=user_input)]}
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")


app, model = initialize_app()


# User input loop
while True:
    #user_input = input("Enter your query (or type 'exit' to quit): ")
    user_input = "What is the weather in prahue"

    if user_input.lower() == 'exit':
        break
    process_input(user_input)
    
