"""ResearchAgent: Retrieves and processes information from the web using free alternatives."""
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field

from utils.config import MAX_SEARCH_RESULTS
from utils.search import search_web
from utils.llm import create_prompt_template, create_completion_chain


class ResearchResult(BaseModel):
    """Output schema for research results."""
    query: str = Field(description="The original search query")
    sources: List[Dict[str, str]] = Field(
        description="List of source documents with URL and content"
    )
    summary: str = Field(description="A summary of the key findings")


class ResearchAgent:
    """Agent that performs web research using free search services and summarizes results."""
    
    def __init__(self, model_name: Optional[str] = None):
        """Initialize the ResearchAgent.
        
        Args:
            model_name: The LLM model to use (not used in the simplified version)
        """
        self.model_name = model_name
        
        # Create the summarization prompt
        self.summarization_prompt = create_prompt_template(
            """You are a research assistant that processes web search results.
            
            Search Query: {query}
            
            Search Results:
            {search_results}
            
            Your task is to:
            1. Analyze the search results
            2. Extract the key information relevant to the query
            3. Remove any duplicated or irrelevant information
            4. Create a comprehensive yet concise summary of the findings
            
            Provide your research summary below:
            """
        )
        
    def _format_source(self, result: Dict[str, Any]) -> Dict[str, str]:
        """Format a search result into a standardized source format."""
        return {
            "title": result.get("title", "Untitled"),
            "url": result.get("url", ""),
            "content": result.get("raw_content", result.get("content", "")),
            "score": "1.0",  # For compatibility with previous data structure
        }
    
    def _clean_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Clean and standardize source data."""
        return [self._format_source(source) for source in sources]
    
    def _create_summary(self, query: str, sources: List[Dict[str, str]]) -> str:
        """Create a summary of the search results."""
        # If no sources, return a message about no results
        if not sources:
            return "No relevant information found for this query."
            
        # Convert sources to a string representation for the prompt
        sources_text = "\n\n".join([
            f"SOURCE {i+1}:\nTitle: {source['title']}\nURL: {source['url']}\nContent: {source['content'][:1000]}..."
            for i, source in enumerate(sources)
        ])
        
        # Generate summary using LLM
        chain_function = create_completion_chain(
            self.summarization_prompt,
            model_name=self.model_name,
            temperature=0.1
        )
        
        result = chain_function({"query": query, "search_results": sources_text})
        return result
    
    def research(self, query: str) -> ResearchResult:
        """Perform research on a given query.
        
        Args:
            query: The search query
            
        Returns:
            A ResearchResult containing sources and summary
        """
        print(f"Starting research for query: {query}")
        
        # Perform web search using our free search utility
        search_results = search_web(query, max_results=MAX_SEARCH_RESULTS)
        
        print(f"Found {len(search_results)} search results")
        
        # Handle case with no search results
        if not search_results:
            # Create a minimal result with a placeholder
            return ResearchResult(
                query=query,
                sources=[{
                    "title": "No results found",
                    "url": "",
                    "content": "No search results were found for this query.",
                    "score": "0.0"
                }],
                summary="No relevant information was found for the query."
            )
        
        # Clean and format sources
        cleaned_sources = self._clean_sources(search_results)
        
        # Create summary
        summary = self._create_summary(query, cleaned_sources)
        
        # Return structured result
        return ResearchResult(
            query=query,
            sources=cleaned_sources,
            summary=summary
        ) 