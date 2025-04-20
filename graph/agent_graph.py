"""LangGraph flow for the dual-agent research system."""
from typing import Dict, List, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain.schema import Document
from langchain.pydantic_v1 import BaseModel, Field

from agents.research_agent import ResearchAgent, ResearchResult
from agents.answer_agent import AnswerAgent, FormattedAnswer


class GraphState(TypedDict):
    """State maintained throughout the agent graph execution."""
    query: str
    research_result: ResearchResult
    answer: FormattedAnswer
    error: str


def create_agent_graph() -> StateGraph:
    """Create the agent graph workflow.
    
    Returns:
        A LangGraph StateGraph representing the workflow
    """
    # Initialize the graph
    workflow = StateGraph(GraphState)
    
    # Initialize agents
    research_agent = ResearchAgent()
    answer_agent = AnswerAgent()
    
    # Define node functions
    def research_node(state: GraphState) -> GraphState:
        """Research agent node that searches and processes information."""
        try:
            query = state["query"]
            research_result = research_agent.research(query)
            return {"research_result": research_result}
        except Exception as e:
            return {"error": f"Research error: {str(e)}"}
    
    def answer_generation_node(state: GraphState) -> GraphState:
        """Answer agent node that creates a formatted answer."""
        try:
            research_result = state["research_result"]
            answer = answer_agent.create_answer(research_result)
            return {"answer": answer}
        except Exception as e:
            return {"error": f"Answer generation error: {str(e)}"}
    
    # Add nodes to the graph
    workflow.add_node("research", research_node)
    workflow.add_node("answer_generation", answer_generation_node)
    
    # Define edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "answer_generation")
    workflow.add_edge("answer_generation", END)
    
    # Define conditional edges for error handling
    def check_for_errors(state: GraphState) -> str:
        """Check if there's an error in the state."""
        if state.get("error"):
            return "error"
        return "continue"
    
    workflow.add_conditional_edges(
        "research",
        check_for_errors,
        {
            "error": END,
            "continue": "answer_generation"
        }
    )
    
    workflow.add_conditional_edges(
        "answer_generation",
        check_for_errors,
        {
            "error": END,
            "continue": END
        }
    )
    
    return workflow


class ResearchSystem:
    """Main system class that orchestrates the research workflow."""
    
    def __init__(self):
        """Initialize the research system."""
        self.graph = create_agent_graph().compile()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query through the agent workflow.
        
        Args:
            query: The user's research query
            
        Returns:
            The final state dictionary containing research results and answer
        """
        # Initialize the state
        initial_state = {
            "query": query,
            "research_result": None,
            "answer": None,
            "error": ""
        }
        
        # Execute the graph
        result = self.graph.invoke(initial_state)
        
        # Return the final state
        return result 