"""
AI handler for processing queries using Gemini API
"""
import google.generativeai as genai
from typing import List, Dict, Optional
import logging
import tiktoken
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIHandler:
    """Handles AI queries using Gemini API"""
    
    def __init__(self):
        self.config = Config()
        self.config.validate()
        
        # Configure Gemini API
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.config.MODEL_NAME)
        
        # Initialize tokenizer for token counting
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            logger.warning(f"Could not initialize tokenizer: {e}")
            self.tokenizer = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Rough estimation: ~4 characters per token
            return len(text) // 4
    
    def select_relevant_chunks(self, chunks: List[Dict], query: str, max_tokens: int = 600) -> List[Dict]:
        """Select most relevant chunks for the query"""
        # Simple keyword-based relevance scoring
        query_words = set(query.lower().split())
        
        scored_chunks = []
        for chunk in chunks:
            chunk_words = set(chunk['text'].lower().split())
            # Calculate overlap score
            overlap = len(query_words.intersection(chunk_words))
            score = overlap / len(query_words) if query_words else 0
            
            scored_chunks.append({
                'chunk': chunk,
                'score': score
            })
        
        # Sort by relevance score
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        
        # Select chunks within token limit
        selected_chunks = []
        total_tokens = 0
        
        for item in scored_chunks:
            chunk = item['chunk']
            chunk_tokens = self.count_tokens(chunk['text'])
            
            if total_tokens + chunk_tokens <= max_tokens:
                selected_chunks.append(chunk)
                total_tokens += chunk_tokens
            else:
                break
        
        logger.info(f"Selected {len(selected_chunks)} chunks ({total_tokens} tokens)")
        return selected_chunks
    
    def create_prompt(self, query: str, chunks: List[Dict], query_type: str = "general") -> str:
        """Create optimized prompt for different query types"""
        
        context = "\n\n".join([f"[Chunk {chunk['id']}]: {chunk['text']}" for chunk in chunks])
        
        if query_type == "direct":
            prompt_template = """You are an AI assistant helping to answer questions about a research paper. 
Based on the following text chunks from the paper, answer the question directly and precisely.

Context from research paper:
{context}

Question: {query}

Instructions:
- Provide a direct, factual answer based on the text
- Quote relevant parts when possible
- If the answer is not in the provided text, say "The information is not available in the provided text"
- Be concise and accurate

Answer:"""

        elif query_type == "indirect":
            prompt_template = """You are an AI assistant helping to analyze a research paper. 
Based on the following text chunks, provide an insightful answer that may require interpretation and synthesis.

Context from research paper:
{context}

Question: {query}

Instructions:
- Analyze and synthesize information from the text
- Provide insights that may not be explicitly stated
- Use your understanding to infer meanings and implications
- Be thoughtful and comprehensive in your response

Answer:"""

        elif query_type == "references":
            prompt_template = """You are an AI assistant helping to identify key references in a research paper.
Based on the following text chunks, identify references that inspire or influence the proposed methodology.

Context from research paper:
{context}

Question: {query}

Instructions:
- Look for citations and references mentioned in the methodology sections
- Identify papers that directly influenced the proposed approach
- Explain how these references contributed to the methodology
- List the references with brief explanations

Answer:"""

        else:  # general
            prompt_template = """You are an AI assistant helping to answer questions about a research paper.
Based on the following text chunks from the paper, provide a comprehensive and accurate answer.

Context from research paper:
{context}

Question: {query}

Instructions:
- Answer based on the provided text
- Be accurate and comprehensive
- Quote relevant parts when helpful
- If information is not available, state this clearly

Answer:"""

        return prompt_template.format(context=context, query=query)
    
    def classify_query_type(self, query: str) -> str:
        """Classify the type of query to optimize response"""
        query_lower = query.lower()
        
        # Keywords for different query types
        direct_keywords = ['what is', 'what are', 'which', 'how many', 'when', 'where', 'who']
        indirect_keywords = ['why', 'how', 'explain', 'analyze', 'insight', 'discovery', 'main']
        reference_keywords = ['reference', 'citation', 'inspire', 'methodology', 'based on', 'influence']
        
        if any(keyword in query_lower for keyword in reference_keywords):
            return "references"
        elif any(keyword in query_lower for keyword in indirect_keywords):
            return "indirect"
        elif any(keyword in query_lower for keyword in direct_keywords):
            return "direct"
        else:
            return "general"
    
    def query(self, question: str, chunks: List[Dict]) -> Dict:
        """Process a query and return AI response"""
        try:
            # Classify query type
            query_type = self.classify_query_type(question)
            logger.info(f"Query classified as: {query_type}")
            
            # Select relevant chunks
            relevant_chunks = self.select_relevant_chunks(chunks, question, self.config.MAX_TOKENS_PER_REQUEST)
            
            if not relevant_chunks:
                return {
                    'success': False,
                    'error': 'No relevant content found for the query'
                }
            
            # Create optimized prompt
            prompt = self.create_prompt(question, relevant_chunks, query_type)
            
            # Count tokens in prompt
            prompt_tokens = self.count_tokens(prompt)
            logger.info(f"Prompt tokens: {prompt_tokens}")
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config.TEMPERATURE,
                    max_output_tokens=400  # Leave room for response
                )
            )
            
            return {
                'success': True,
                'answer': response.text,
                'query_type': query_type,
                'chunks_used': len(relevant_chunks),
                'prompt_tokens': prompt_tokens
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'success': False,
                'error': str(e)
            }
