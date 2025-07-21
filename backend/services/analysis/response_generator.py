"""
Enhanced response generation for AML/FT compliance queries.

This module provides structured response generation with cross-jurisdictional
analysis and source attribution.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class StructuredResponseGenerator:
    def __init__(self):
        self.confidence_thresholds = {
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
    
    def generate_response(self, query: str, search_results: List[Dict]) -> Dict[str, Any]:
        """
        Generates a structured response from search results.
        """
        try:
            response = {
                'direct_answer': self.extract_main_answer(search_results),
                'jurisdiction_specific': self.get_jurisdiction_requirements(search_results),
                'cross_jurisdiction': self.get_comparative_analysis(search_results),
                'sources': self.format_sources(search_results),
                'confidence': self.calculate_confidence_score(search_results)
            }
            
            logger.info(f"Generated structured response with confidence: {response['confidence']}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating structured response: {e}")
            return self.generate_error_response()
    
    def extract_main_answer(self, search_results: List[Dict]) -> Dict[str, Any]:
        """
        Extracts the main answer from search results.
        """
        main_answer = {
            'summary': self.generate_summary(search_results),
            'key_points': self.extract_key_points(search_results),
            'relevance_score': self.calculate_relevance(search_results)
        }
        return main_answer
    
    def get_jurisdiction_requirements(self, search_results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Extracts jurisdiction-specific requirements.
        """
        requirements = {
            'br': self.extract_brazilian_requirements(search_results),
            'us': self.extract_us_requirements(search_results),
            'eu': self.extract_eu_requirements(search_results)
        }
        return requirements
    
    def get_comparative_analysis(self, search_results: List[Dict]) -> Dict[str, Any]:
        """
        Performs cross-jurisdictional analysis.
        """
        analysis = {
            'similarities': self.find_common_requirements(search_results),
            'differences': self.find_jurisdiction_differences(search_results),
            'unique_aspects': self.identify_unique_requirements(search_results)
        }
        return analysis
    
    def format_sources(self, search_results: List[Dict]) -> List[Dict[str, Any]]:
        """
        Formats source citations and references.
        """
        sources = []
        for result in search_results:
            source = {
                'document': result.get('filename', ''),
                'jurisdiction': result.get('jurisdiction', ''),
                'relevance': result.get('score', 0.0),
                'excerpt': self.format_excerpt(result.get('content', ''))
            }
            sources.append(source)
        return sources
    
    def calculate_confidence_score(self, search_results: List[Dict]) -> float:
        """
        Calculates overall confidence score for the response.
        """
        if not search_results:
            return 0.0
            
        scores = [result.get('score', 0.0) for result in search_results]
        avg_score = sum(scores) / len(scores)
        
        # Apply weights based on source quality
        weighted_score = self.apply_source_weights(avg_score, search_results)
        
        return min(1.0, weighted_score)
    
    def generate_error_response(self) -> Dict[str, Any]:
        """
        Generates a structured error response.
        """
        return {
            'direct_answer': {
                'summary': 'Unable to generate response',
                'key_points': [],
                'relevance_score': 0.0
            },
            'jurisdiction_specific': {},
            'cross_jurisdiction': {},
            'sources': [],
            'confidence': 0.0
        }
    
    def format_excerpt(self, content: str, max_length: int = 500) -> str:
        """
        Formats content excerpt with proper length and context.
        """
        if not content:
            return ''
            
        if len(content) <= max_length:
            return content
            
        return content[:max_length] + '...'
    
    def apply_source_weights(self, base_score: float, search_results: List[Dict]) -> float:
        """
        Applies quality weights to the confidence score.
        """
        weights = {
            'primary_source': 1.2,
            'recent_document': 1.1,
            'official_translation': 1.0,
            'unofficial_source': 0.8
        }
        
        weighted_score = base_score
        for result in search_results:
            if self.is_primary_source(result):
                weighted_score *= weights['primary_source']
            if self.is_recent_document(result):
                weighted_score *= weights['recent_document']
                
        return weighted_score 