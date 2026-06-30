from workflows.langgraph_workflow import graph


def execute(state):

    return graph.invoke(state)