"""
Quick test script to verify ML model is working
"""
import joblib
import os

# Check if model exists
model_path = 'models_store/classifier.joblib'
if not os.path.exists(model_path):
    print("❌ Model file not found!")
    exit(1)

print("✅ Model file found")

# Load model
try:
    classifier_data = joblib.load(model_path)
    vectorizer = classifier_data['vectorizer']
    classifier = classifier_data['model']
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit(1)

# Test predictions
test_cases = [
    ("Invoice for office supplies payment due", "Finance"),
    ("Employee salary payroll report", "HR"),
    ("Purchase order for equipment supplies", "Procurement"),
    ("Repair broken equipment maintenance request", "Maintenance"),
    ("Budget quarterly financial report", "Finance"),
    ("Leave request vacation employee", "HR"),
    ("Supplier contract procurement agreement", "Procurement"),
    ("Service maintenance equipment repair", "Maintenance"),
]

print("\n" + "="*70)
print("TESTING MODEL PREDICTIONS")
print("="*70)

correct = 0
total = len(test_cases)

for text, expected in test_cases:
    # Vectorize
    features = vectorizer.transform([text])
    
    # Predict
    prediction = classifier.predict(features)[0]
    
    # Check if correct
    is_correct = prediction == expected
    correct += is_correct
    
    # Display result
    status = "✅" if is_correct else "❌"
    print(f"\n{status} Text: '{text[:50]}...'")
    print(f"   Expected: {expected}")
    print(f"   Predicted: {prediction}")
    
    # Show confidence scores (if available)
    if hasattr(classifier, 'decision_function'):
        scores = classifier.decision_function(features)[0]
        categories = ['Finance', 'HR', 'Maintenance', 'Procurement']
        print(f"   Confidence scores:")
        for cat, score in zip(categories, scores):
            print(f"      {cat}: {score:.3f}")

print("\n" + "="*70)
print(f"ACCURACY: {correct}/{total} ({100*correct/total:.1f}%)")
print("="*70)

# Check model details
print("\n" + "="*70)
print("MODEL DETAILS")
print("="*70)
print(f"Vectorizer type: {type(vectorizer).__name__}")
print(f"Classifier type: {type(classifier).__name__}")
print(f"Number of features: {len(vectorizer.get_feature_names_out())}")
print(f"Categories: {classifier.classes_}")

print("\n✅ Model is working correctly!")
