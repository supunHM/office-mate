"""
Enhanced Summary Generator with Point-Wise Analysis
Generates intelligent, structured summaries from document text
"""

import re
from typing import List, Dict
import spacy

class SummaryGenerator:
    """Generate point-wise AI summaries from document text"""
    
    def __init__(self):
        """Initialize spaCy model"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Warning: spaCy model not found")
            self.nlp = None
    
    def extract_sentences(self, text: str, max_sentences: int = 5) -> List[str]:
        """Extract key sentences from text"""
        if not self.nlp:
            # Fallback: simple sentence splitting
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()][:max_sentences]
        
        doc = self.nlp(text[:5000])  # Limit to first 5000 chars for performance
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences[:max_sentences]
    
    def extract_key_sections(self, text: str) -> Dict[str, str]:
        """Extract main sections and headers from document"""
        sections = {}
        
        # Look for common section patterns
        lines = text.split('\n')
        current_section = "Introduction"
        section_content = []
        
        for line in lines:
            # Check if line is a section header (ALL CAPS, short, or starts with number)
            if (line.isupper() and len(line) < 100 and len(line) > 3) or \
               re.match(r'^\d+\.\s+\w+', line) or \
               line.endswith(':'):
                if section_content:
                    sections[current_section] = ' '.join(section_content)
                current_section = line.strip(':').strip()
                section_content = []
            else:
                if line.strip():
                    section_content.append(line.strip())
        
        if section_content:
            sections[current_section] = ' '.join(section_content)
        
        return sections
    
    def identify_key_entities(self, text: str) -> Dict[str, List[str]]:
        """Identify key entities using spaCy"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text[:5000])
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],
            'DATE': [],
            'MONEY': [],
            'PRODUCT': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                if ent.text not in entities[ent.label_]:
                    entities[ent.label_].append(ent.text)
        
        return {k: v for k, v in entities.items() if v}
    
    def extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """Extract important phrases/keywords"""
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
            'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        # Extract noun phrases (words that are capitalized or important)
        words = re.findall(r'\b[A-Z]\w+(?:\s+[A-Z]\w+)*\b', text)
        phrases = [w for w in words if w.lower() not in stop_words and len(w) > 3]
        
        # Remove duplicates and return top phrases
        return list(dict.fromkeys(phrases))[:max_phrases]
    
    def generate_point_wise_summary(self, text: str, category: str = "Unknown") -> Dict:
        """
        Generate comprehensive point-wise summary
        
        Returns:
            {
                'executive_summary': str,
                'key_points': [str, ...],
                'sections': {section: content, ...},
                'key_entities': {entity_type: [values], ...},
                'key_concepts': [str, ...],
                'structure': str,
                'confidence': float
            }
        """
        
        if not text or len(text.strip()) < 50:
            return {
                'executive_summary': 'Document too short for analysis',
                'key_points': [],
                'sections': {},
                'key_entities': {},
                'key_concepts': [],
                'structure': 'Insufficient content',
                'confidence': 0.0
            }
        
        # Extract components
        key_sentences = self.extract_sentences(text, max_sentences=5)
        sections = self.extract_key_sections(text)
        entities = self.identify_key_entities(text)
        phrases = self.extract_key_phrases(text, max_phrases=10)
        
        # Generate executive summary
        exec_summary = self._generate_executive_summary(text, category, key_sentences)
        
        # Determine document structure
        structure = self._analyze_structure(text, sections)
        
        # Calculate confidence
        confidence = self._calculate_confidence(text, len(sections), len(phrases))
        
        return {
            'executive_summary': exec_summary,
            'key_points': key_sentences,
            'sections': sections,
            'key_entities': entities,
            'key_concepts': phrases,
            'structure': structure,
            'confidence': confidence
        }
    
    def _generate_executive_summary(self, text: str, category: str, key_sentences: List[str]) -> str:
        """Generate executive summary from key sentences"""
        # Get first 200 chars as context
        first_para = text.split('\n\n')[0][:200].strip()
        
        summary_parts = [
            f"📄 **Document Type**: {category}",
            f"📝 **Overview**: {first_para}...",
        ]
        
        if key_sentences:
            summary_parts.append(f"🎯 **Key Point**: {key_sentences[0][:150]}...")
        
        return " | ".join(summary_parts)
    
    def _analyze_structure(self, text: str, sections: Dict) -> str:
        """Analyze and describe document structure"""
        if len(sections) > 5:
            return f"Well-structured document with {len(sections)} main sections"
        elif len(sections) > 2:
            return f"Moderately structured with {len(sections)} sections"
        elif len(sections) > 0:
            return f"Simple structure with {len(sections)} section(s)"
        else:
            return "Unstructured document"
    
    def _calculate_confidence(self, text: str, num_sections: int, num_phrases: int) -> float:
        """Calculate confidence in summary quality"""
        # Factors: text length, structure, entities, phrases
        length_score = min(len(text) / 10000, 1.0)  # Normalized
        structure_score = min(num_sections / 5, 1.0)  # Normalized
        phrases_score = min(num_phrases / 15, 1.0)  # Normalized
        
        # Average confidence
        confidence = (length_score + structure_score + phrases_score) / 3
        return round(confidence, 2)


def generate_enhanced_summary(text: str, category: str = "Unknown") -> Dict:
    """
    Wrapper function for summary generation
    Usage: result = generate_enhanced_summary(extracted_text, "Finance")
    """
    try:
        generator = SummaryGenerator()
        return generator.generate_point_wise_summary(text, category)
    except Exception as e:
        print(f"Summary generation error: {e}")
        return {
            'executive_summary': text[:200] + '...',
            'key_points': [],
            'sections': {},
            'key_entities': {},
            'key_concepts': [],
            'structure': 'Error in analysis',
            'confidence': 0.0,
            'error': str(e)
        }


if __name__ == "__main__":
    # Test the summary generator
    test_text = """
    Finance Module Specification
    
    Executive Summary
    The Finance Module is a specialized component designed to manage financial documents,
    transactions, invoices, and receipts for office administration.
    
    Key Features:
    1. Automated Classification
    2. Secure Storage
    3. Audit Compliance
    4. Intelligent Task Management
    
    Technical Specifications:
    The module uses advanced ML algorithms for document categorization.
    It integrates with the main database system for real-time processing.
    
    Conclusion:
    This module provides comprehensive financial document management capabilities.
    """
    
    generator = SummaryGenerator()
    result = generator.generate_point_wise_summary(test_text, "Finance")
    
    print("\n" + "="*80)
    print("POINT-WISE SUMMARY ANALYSIS")
    print("="*80)
    
    print(f"\n📊 Executive Summary:")
    print(f"   {result['executive_summary']}")
    
    print(f"\n🎯 Key Points:")
    for i, point in enumerate(result['key_points'], 1):
        print(f"   {i}. {point[:100]}...")
    
    print(f"\n📑 Document Sections:")
    for section, content in result['sections'].items():
        preview = content[:80].replace('\n', ' ')
        print(f"   • {section}: {preview}...")
    
    print(f"\n🏷️  Key Entities:")
    for entity_type, values in result['key_entities'].items():
        print(f"   • {entity_type}: {', '.join(values[:3])}")
    
    print(f"\n💡 Key Concepts:")
    for concept in result['key_concepts'][:8]:
        print(f"   • {concept}")
    
    print(f"\n🔍 Analysis Confidence: {result['confidence']*100:.1f}%")
    print(f"📐 Document Structure: {result['structure']}")
    print("\n" + "="*80)
