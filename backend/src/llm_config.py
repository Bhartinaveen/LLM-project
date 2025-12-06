"""
LLM Configuration Module
Handles Google Gemini integration and LLM initialization
"""

import os
import logging
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LLMConfig:
    """Configuration for LLM models"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        """
        Initialize LLM configuration
        
        Args:
            api_key: Google Gemini API key
            model: Model name (default: gemini-1.5-flash)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. LLM features will fail if used.")
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        logger.info(f"LLM Config initialized with model: {self.model}")

    def get_llm(self) -> Any:
        """
        Get initialized LLM instance
        
        Returns:
            Gemini model wrapper instance
        """
        import google.generativeai as genai

        if not self.api_key:
             raise ValueError("GEMINI_API_KEY is missing. Cannot use LLM.")

        genai.configure(api_key=self.api_key)

        class GeminiWrapper:
            def __init__(self, model_name: str, temperature: float, max_tokens: int):
                self.model = genai.GenerativeModel(model_name)
                self.temperature = temperature
                self.max_tokens = max_tokens

            def invoke(self, prompt: str):
                # Generate content using Gemini
                generation_config = genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
                
                resp = self.model.generate_content(
                    prompt,
                    generation_config=generation_config,
                )
                
                content = ""
                try:
                    content = resp.text.strip()
                except Exception:
                    # Fallback to textual content if structure differs
                    content = str(resp)

                # Return an object with `.content` attribute for compatibility
                return type("Resp", (), {"content": content})

        return GeminiWrapper(self.model, self.temperature, self.max_tokens)


def initialize_llm(model: str = "gemini-2.0-flash") -> Any:
    """
    Convenience function to initialize LLM
    
    Args:
        model: Model name
        
    Returns:
        Gemini model wrapper instance
    """
    config = LLMConfig(model=model)
    return config.get_llm()
