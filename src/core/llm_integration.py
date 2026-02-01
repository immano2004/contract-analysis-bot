"""
LLM integration for enhanced contract analysis
"""
import os
import logging
from typing import Optional
from src.models.contract_models import Clause, ContractAnalysis
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class LLMIntegration:
    """Integrate Claude or GPT for legal reasoning"""
    
    def __init__(self, provider: str = "claude", api_key: Optional[str] = None):
        """
        Initialize LLM integration
        
        Args:
            provider: "claude" or "openai"
            api_key: API key (or use environment variable)
        """
        self.provider = provider.lower()
        
        if self.provider == "claude":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                logger.warning("ANTHROPIC_API_KEY not set")
                self.client = None
            else:
                try:
                    from anthropic import Anthropic
                    self.client = Anthropic(api_key=self.api_key)
                except ImportError:
                    logger.warning("anthropic package not installed")
                    self.client = None
        
        elif self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                logger.warning("OPENAI_API_KEY not set")
                self.client = None
            else:
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=self.api_key)
                except ImportError:
                    logger.warning("openai package not installed")
                    self.client = None
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def generate_summary(self, contract_text: str, contract_type: str) -> str:
        """
        Generate a summary of the contract using LLM
        
        Args:
            contract_text: The contract text
            contract_type: Type of contract
            
        Returns:
            Summary text
        """
        if not self.client:
            return "Summary generation not available (LLM not configured)"
        
        prompt = f"""Please provide a brief 2-3 sentence summary of this {contract_type} contract. 
Focus on the main purpose and key obligations:

{contract_text[:2000]}..."""
        
        try:
            if self.provider == "claude":
                message = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Summary generation failed"
    
    def generate_plain_language_explanation(self, clause_text: str, clause_category: str) -> str:
        """
        Generate plain language explanation of a clause
        
        Args:
            clause_text: The clause text
            clause_category: Category of the clause
            
        Returns:
            Plain language explanation
        """
        if not self.client:
            return "Explanation generation not available (LLM not configured)"
        
        prompt = f"""Explain this {clause_category} clause in simple business language for an Indian SME owner.
Keep it to 2-3 sentences and avoid legal jargon:

{clause_text}"""
        
        try:
            if self.provider == "claude":
                message = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=100,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Explanation generation failed"
    
    def generate_renegotiation_suggestions(self, clause_text: str, risk_level: str) -> str:
        """
        Generate renegotiation suggestions for high-risk clauses
        
        Args:
            clause_text: The clause text
            risk_level: Risk level of the clause
            
        Returns:
            Suggested negotiation points
        """
        if not self.client:
            return "Suggestions not available (LLM not configured)"
        
        prompt = f"""For this {risk_level}-risk clause in an Indian contract, suggest 1-2 specific negotiation points 
to make it more favorable for the business. Keep suggestions practical and concise:

{clause_text}"""
        
        try:
            if self.provider == "claude":
                message = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=120,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=120
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return "Suggestion generation failed"
    
    def check_compliance(self, clause_text: str, contract_type: str) -> list:
        """
        Check clause compliance with Indian laws
        
        Args:
            clause_text: The clause text
            contract_type: Type of contract
            
        Returns:
            List of compliance concerns
        """
        if not self.client:
            return []
        
        prompt = f"""Check if this clause in an Indian {contract_type} contract complies with Indian laws.
List any potential legal concerns (1-2 concerns max). Be specific but concise:

{clause_text}"""
        
        try:
            if self.provider == "claude":
                message = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = message.content[0].text
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150
                )
                response_text = response.choices[0].message.content
            
            # Parse response to extract concerns
            concerns = [line.strip() for line in response_text.split('\n') if line.strip()]
            return concerns
        except Exception as e:
            logger.error(f"Error checking compliance: {e}")
            return []
