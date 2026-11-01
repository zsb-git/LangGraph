from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BMIState(TypedDict):
    weight: float
    height: float
    bmi: float
    label: str


def calculate_bmi(state: BMIState) -> BMIState:
    weight = state["weight"]
    height = state["height"]
    bmi = weight / (height ** 2)
    state["bmi"] = round(bmi, 2)
    return state

def label_bmi(state: BMIState) -> BMIState:
    bmi = state["bmi"]
    if bmi < 18.5:
        state["label"] = "Underweight"
    elif 18.5 <= bmi < 24.9:
        state["label"] = "Normal weight"
    elif 25 <= bmi < 29.9:
        state["label"] = "Overweight"
    else:
        state["label"] = "Obesity"
    return state

# define the state graph
bmi_graph = StateGraph(BMIState)

# ADD nodes to the graph

bmi_graph.add_node("calculate_bmi", calculate_bmi)
bmi_graph.add_node("label_bmi", label_bmi)

# add edges to the graph
bmi_graph.add_edge(START, "calculate_bmi")
bmi_graph.add_edge("calculate_bmi", "label_bmi")
bmi_graph.add_edge("label_bmi", END)

workflow = bmi_graph.compile()

initial_state = {"weight": 83, "height": 1.80}
final_state = workflow.invoke(initial_state)

print(f"Final State: {final_state}")