from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class NegotiationGraphState(TypedDict):
    buyer_message: str
    seller_message: str
    status: str


def build_negotiation_graph():
    graph = StateGraph(NegotiationGraphState)

    def buyer_node(state: NegotiationGraphState) -> NegotiationGraphState:
        return {
            **state,
            "buyer_message": "buyer proposes revised terms",
            "status": "buyer_acted",
        }

    def seller_node(state: NegotiationGraphState) -> NegotiationGraphState:
        return {
            **state,
            "seller_message": "seller evaluates and responds",
            "status": "seller_acted",
        }

    graph.add_node("buyer", buyer_node)
    graph.add_node("seller", seller_node)
    graph.add_edge(START, "buyer")
    graph.add_edge("buyer", "seller")
    graph.add_edge("seller", END)
    return graph.compile()
