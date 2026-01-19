"""
Enhanced Classification Module with Detailed Reporting
Provides confidence scores, probability distributions, and feature analysis
"""

import numpy as np
from typing import Dict, List, Tuple
import joblib

class EnhancedClassifier:
    """Enhanced document classifier with detailed analysis"""
    
    def __init__(self, model_path='models_store/enhanced_classifier.joblib'):
        """Initialize classifier by loading saved models"""
        self.model_data = joblib.load(model_path)
        self.vectorizer = self.model_data['vectorizer']
        self.ensemble_model = self.model_data['ensemble_model']
        self.svm_model = self.model_data['svm_model']
        self.rf_model = self.model_data['rf_model']
        self.categories = self.model_data['categories']
        self.feature_names = self.model_data['feature_names']
        
    def classify_with_details(self, text: str) -> Dict:
        """
        Classify document and return detailed analysis
        
        Returns:
            {
                'predicted_category': str,
                'confidence_score': float (0-1),
                'probability_distribution': {category: probability, ...},
                'model_agreement': {model_name: prediction, ...},
                'top_features': [{'feature': str, 'weight': float}, ...],
                'analysis': str
            }
        """
        
        if not text or len(text.strip()) < 10:
            return {
                'predicted_category': 'unknown',
                'confidence_score': 0.0,
                'probability_distribution': {cat: 0.0 for cat in self.categories},
                'model_agreement': {},
                'top_features': [],
                'analysis': 'Text too short for reliable classification',
                'warning': 'Insufficient text'
            }
        
        # Vectorize text
        text_vec = self.vectorizer.transform([text])
        
        # Get predictions from all models
        ensemble_pred = self.ensemble_model.predict(text_vec)[0]
        svm_pred = self.svm_model.predict(text_vec)[0]
        rf_pred = self.rf_model.predict(text_vec)[0]
        
        # Get probability scores from Random Forest
        rf_probabilities = self.rf_model.predict_proba(text_vec)[0]
        
        # Create probability distribution
        prob_dist = {self.categories[i]: float(rf_probabilities[i]) for i in range(len(self.categories))}
        
        # Get confidence score (highest probability)
        predicted_idx = np.argmax(rf_probabilities)
        confidence_score = float(rf_probabilities[predicted_idx])
        
        # Check model agreement
        model_agreement = {
            'svm': svm_pred,
            'random_forest': rf_pred,
            'ensemble': ensemble_pred,
            'consensus': ensemble_pred
        }
        
        # Determine if models agree
        models_agree = len(set(model_agreement.values())) == 1
        agreement_strength = 'High' if models_agree else 'Mixed'
        
        # Get top contributing features
        top_features = self._get_top_features(text, text_vec)
        
        # Generate analysis
        analysis = self._generate_analysis(
            ensemble_pred,
            confidence_score,
            prob_dist,
            model_agreement,
            models_agree
        )
        
        return {
            'predicted_category': ensemble_pred,
            'confidence_score': confidence_score,
            'confidence_percentage': f"{confidence_score*100:.2f}%",
            'confidence_level': self._get_confidence_level(confidence_score),
            'probability_distribution': prob_dist,
            'probability_ranking': sorted(prob_dist.items(), key=lambda x: x[1], reverse=True),
            'model_agreement': model_agreement,
            'models_agree': models_agree,
            'agreement_strength': agreement_strength,
            'top_features': top_features,
            'analysis': analysis,
            'document_length': len(text),
            'processed_at': __import__('datetime').datetime.now().isoformat()
        }
    
    def _get_top_features(self, text: str, text_vec) -> List[Dict]:
        """Extract top features contributing to classification"""
        
        # Get feature scores from the text vector
        dense_vec = text_vec.toarray()[0]
        top_indices = np.argsort(dense_vec)[-10:][::-1]
        
        top_features = []
        for idx in top_indices:
            if dense_vec[idx] > 0:
                feature = self.feature_names[idx]
                weight = float(dense_vec[idx])
                top_features.append({
                    'feature': feature,
                    'weight': weight,
                    'weight_percentage': f"{(weight/dense_vec.max()*100):.1f}%"
                })
        
        return top_features
    
    def _get_confidence_level(self, score: float) -> str:
        """Convert confidence score to level"""
        if score >= 0.85:
            return 'Very High'
        elif score >= 0.70:
            return 'High'
        elif score >= 0.55:
            return 'Medium'
        elif score >= 0.40:
            return 'Low'
        else:
            return 'Very Low'
    
    def _generate_analysis(
        self, 
        category: str,
        confidence: float,
        prob_dist: Dict,
        model_agreement: Dict,
        models_agree: bool
    ) -> str:
        """Generate human-readable analysis"""
        
        analysis_points = []
        
        # Predicted category analysis
        analysis_points.append(f"✓ Document classified as: {category}")
        
        # Confidence analysis
        conf_pct = confidence * 100
        if confidence >= 0.85:
            analysis_points.append(f"✓ High confidence ({conf_pct:.1f}%) - Classification is very reliable")
        elif confidence >= 0.70:
            analysis_points.append(f"✓ Good confidence ({conf_pct:.1f}%) - Classification is reliable")
        elif confidence >= 0.55:
            analysis_points.append(f"⚠ Medium confidence ({conf_pct:.1f}%) - Document may have mixed characteristics")
        else:
            analysis_points.append(f"⚠ Low confidence ({conf_pct:.1f}%) - Manual review recommended")
        
        # Model agreement analysis
        if models_agree:
            analysis_points.append(f"✓ All models agree on classification - Strong consensus")
        else:
            analysis_points.append(f"⚠ Model disagreement detected - SVM: {model_agreement['svm']}, RF: {model_agreement['random_forest']}")
        
        # Alternative categories
        sorted_probs = sorted(prob_dist.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_probs) > 1:
            alternatives = [f"{cat} ({prob*100:.1f}%)" for cat, prob in sorted_probs[1:3]]
            analysis_points.append(f"○ Alternative classifications: {', '.join(alternatives)}")
        
        return " | ".join(analysis_points)


def classify_document_enhanced(text: str) -> Dict:
    """
    Wrapper function for document classification
    Usage in flask_documents_api.py
    """
    try:
        classifier = EnhancedClassifier()
        result = classifier.classify_with_details(text)
        return result
    except Exception as e:
        return {
            'predicted_category': 'unknown',
            'confidence_score': 0.0,
            'error': str(e),
            'fallback': True
        }


if __name__ == "__main__":
    # Test the enhanced classifier
    print("Testing Enhanced Classifier...\n")
    
    test_texts = [
        "Invoice for services rendered Amount due 5000 rupees Payment required",
        "Employee leave application for vacation days Annual leave approval",
        "Purchase order for office supplies Equipment vendor quotation provided",
        "Air conditioning system maintenance Repair needed urgently",
    ]
    
    classifier = EnhancedClassifier()
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}: {text[:60]}...")
        print(f"{'='*80}")
        
        result = classifier.classify_with_details(text)
        
        print(f"\n📊 Classification Results:")
        print(f"   Predicted Category: {result['predicted_category']}")
        print(f"   Confidence: {result['confidence_percentage']} ({result['confidence_level']})")
        print(f"\n📈 Probability Distribution:")
        for cat, prob in result['probability_ranking'][:3]:
            bar = '█' * int(prob * 30)
            print(f"   {cat:15} {prob*100:6.2f}% {bar}")
        
        print(f"\n🤖 Model Agreement:")
        for model, pred in result['model_agreement'].items():
            status = "✓" if model == 'consensus' else "○"
            print(f"   {status} {model:15} {pred}")
        
        print(f"\n🔑 Top Contributing Features:")
        for feat in result['top_features'][:5]:
            print(f"   • {feat['feature']:20} (weight: {feat['weight']:.3f})")
        
        print(f"\n💡 Analysis:")
        print(f"   {result['analysis']}")
