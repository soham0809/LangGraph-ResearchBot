"""A simple, local mock LLM for demo purposes that doesn't require API keys."""
from typing import Dict, Any, Optional, List
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import PromptTemplate


class SimpleLLM:
    """Simple mock LLM for demonstration purposes."""
    
    def __init__(self, temperature=0.1):
        """Initialize the simple LLM."""
        self.temperature = temperature
    
    def invoke(self, prompt: str) -> str:
        """Process the prompt and return a response.
        
        Args:
            prompt: The input prompt
            
        Returns:
            A generated response
        """
        # Generate a basic response based on the prompt
        if "search results" in prompt.lower():
            # For research summarization
            return self._generate_research_summary(prompt)
        else:
            # For answer generation
            return self._generate_answer(prompt)
    
    def _generate_research_summary(self, prompt: str) -> str:
        """Generate a research summary."""
        query = prompt.split("Search Query:")[1].split("\n")[0].strip() if "Search Query:" in prompt else "unknown query"
        
        return f"""Based on the search results, here are the key findings about {query}:

1. Quantum computing has seen significant advances in quantum error correction, making quantum systems more reliable.

2. There have been breakthroughs in scaling quantum bits (qubits), with companies like IBM and Google achieving new milestones in qubit count and quality.

3. Quantum advantage demonstrations have shown quantum computers solving specific problems faster than classical supercomputers.

4. New quantum algorithms have been developed for optimization, machine learning, and simulation applications.

5. Quantum computing is being increasingly applied to real-world problems in chemistry, materials science, and finance.

These advances suggest quantum computing is moving from purely theoretical research toward practical applications, though widespread commercial use is still years away."""
    
    def _generate_answer(self, prompt: str) -> str:
        """Generate a comprehensive answer with citations."""
        query = prompt.split("following query:")[1].split("\n")[0].strip() if "following query:" in prompt else "recent advances in quantum computing"
        
        return f"""# Recent Advances in Quantum Computing

Quantum computing has seen remarkable progress in recent years. This report outlines the major recent advances in this field.

## Quantum Error Correction and Fault Tolerance

One of the most significant challenges in quantum computing has been managing errors and decoherence. Recent advances in quantum error correction have made substantial progress in addressing these issues [Source 1].

IBM recently announced their new quantum error correction techniques that have significantly improved the reliability of their quantum systems, potentially paving the way for fault-tolerant quantum computing [Source 2].

## Scaling Quantum Systems

There has been impressive progress in scaling quantum bits (qubits):

- IBM unveiled their 127-qubit Eagle processor in 2021 and has a roadmap to reach 1,000+ qubits [Source 1]
- Google has improved their Sycamore processor and continues to scale their quantum systems [Source 3]
- Quantum startups like IonQ and PsiQuantum have made advances in different quantum architectures that show promise for scalability [Source 2]

## Quantum Advantage Demonstrations

Several experiments have demonstrated "quantum advantage" (sometimes called "quantum supremacy"):

- Google's 2019 quantum advantage experiment has been followed by more practical demonstrations [Source 3]
- Chinese researchers achieved quantum advantage with photonic quantum computers for specific problems [Source 4]
- These demonstrations show quantum computers solving particular problems faster than classical supercomputers [Source 3]

## Quantum Algorithms and Software

The software side of quantum computing has seen significant advances:

- New quantum algorithms for optimization problems have been developed [Source 2]
- Quantum machine learning techniques have advanced considerably [Source 1]
- Simulation algorithms for chemistry and materials science have improved [Source 5]

## Commercial and Practical Applications

Quantum computing is moving closer to practical applications:

- Financial institutions are exploring quantum algorithms for portfolio optimization and risk analysis [Source 4]
- Pharmaceutical companies are using quantum computing for drug discovery [Source 5]
- Materials science researchers are applying quantum algorithms to develop new materials [Source 1]

## Conclusion

While universal fault-tolerant quantum computers are still years away, the field has made remarkable progress. These recent advances suggest quantum computing is transitioning from a purely theoretical field to one with increasingly practical applications.

The next few years will likely see continued improvements in qubit count, coherence times, and error rates, bringing us closer to realizing the full potential of quantum computing technology [Source 3].
"""


def create_prompt_template(template: str) -> PromptTemplate:
    """Create a prompt template from a string template."""
    return PromptTemplate.from_template(template)


def create_completion_chain(prompt_template: PromptTemplate, model_name: Optional[str] = None, temperature: float = 0.1):
    """Create a completion chain using a prompt and the simple LLM.
    
    Args:
        prompt_template: The prompt template
        model_name: Not used in this simple implementation
        temperature: Controls randomness (not actually used in simple implementation)
        
    Returns:
        A chain that processes the prompt
    """
    llm = SimpleLLM(temperature=temperature)
    
    def process_with_simple_llm(prompt_args):
        formatted_prompt = prompt_template.format(**prompt_args)
        return llm.invoke(formatted_prompt)
    
    return process_with_simple_llm 