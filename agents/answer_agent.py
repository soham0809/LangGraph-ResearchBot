"""AnswerAgent: Takes research results and creates structured, cited answers using free LLMs."""
from typing import Dict, List, Optional
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field

from utils.llm import create_prompt_template, create_completion_chain
from agents.research_agent import ResearchResult


class FormattedAnswer(BaseModel):
    """Output schema for formatted answers."""
    answer: str = Field(description="The formatted answer with citations")
    sources: List[Dict[str, str]] = Field(description="The sources used in the answer")


class AnswerAgent:
    """Agent that formats research results into comprehensive answers with citations."""
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the AnswerAgent.
        
        Args:
            model_name: The LLM model to use (not used in the simplified version)
        """
        self.model_name = model_name
        
        # Create the answer generation prompt
        self.answer_prompt = create_prompt_template(
            """You are an expert research analyst that creates comprehensive, accurate, and well-cited responses.
            
            You have been provided with research results about the following query:
            {query}
            
            Research summary:
            {summary}
            
            Source documents:
            {sources}
            
            Your task is to:
            1. Create a comprehensive answer to the original query using the research provided.
            2. Include inline citations for all factual claims using the format [Source X] where X is the source number.
            3. Be objective, thorough, and accurate, relying strictly on the source material.
            4. Structure your response logically with clear sections, paragraphs, and bullet points as needed.
            5. If the sources contain conflicting information, acknowledge this and present multiple perspectives.
            6. If the information is insufficient to fully answer the query, clearly state what's missing.
            
            Provide your well-formatted answer below:
            """
        )
    
    def _format_sources_for_prompt(self, sources: List[Dict[str, str]]) -> str:
        """Format sources for inclusion in the prompt."""
        if not sources:
            return "No sources available."
            
        return "\n\n".join([
            f"SOURCE {i+1}:\nTitle: {source['title']}\nURL: {source['url']}"
            for i, source in enumerate(sources)
        ])
    
    def create_answer(self, research_result: ResearchResult) -> FormattedAnswer:
        """Create a comprehensive answer based on research results.
        
        Args:
            research_result: The ResearchResult from the ResearchAgent
            
        Returns:
            A FormattedAnswer containing the answer and sources used
        """
        print("Creating answer from research results...")
        
        # Check for valid research result
        if research_result is None:
            # Handle missing research result gracefully
            return FormattedAnswer(
                answer="Unable to generate an answer due to missing research results.",
                sources=[]
            )
            
        # Ensure sources exists
        sources = research_result.sources if hasattr(research_result, 'sources') else []
        
        sources_formatted = self._format_sources_for_prompt(sources)
        
        # Create and run the chain
        chain_function = create_completion_chain(
            self.answer_prompt,
            model_name=self.model_name,
            temperature=0.2
        )
        
        # Generate the answer
        try:
            result = chain_function({
                "query": research_result.query,
                "summary": research_result.summary,
                "sources": sources_formatted
            })
        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            result = f"Error generating a proper answer. Summary of findings: {research_result.summary}"
        
        return FormattedAnswer(
            answer=result,
            sources=sources
        ) 