"""
Train a simple document classifier for Office Mate
Categories: Finance, HR, Procurement, Maintenance
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
import joblib
import os

# Sample training data with more examples
train_texts = [
    # Finance documents
    "Invoice for payment of services rendered Amount due 5000 rupees",
    "Financial statement quarterly report revenue expenses profit loss",
    "Receipt for purchase payment confirmation transaction completed",
    "Budget proposal financial planning annual expenses allocation",
    "Tax document income tax filing annual return financial year",
    "Bank statement account balance transactions deposits withdrawals",
    "Expense report reimbursement travel costs business expenses",
    "Payment voucher cash disbursement approved amount paid",
    
    # HR documents
    "Employee leave application vacation days annual leave approval",
    "Resignation letter notice period last working day employment termination",
    "Job offer letter employment contract salary position appointment",
    "Performance appraisal employee evaluation annual review rating",
    "Attendance record working hours time sheet employee presence",
    "Training certificate course completion employee development program",
    "Salary slip payslip monthly wages deductions net pay",
    "Employee handbook company policies code of conduct rules",
    
    # Procurement documents
    "Purchase order for office supplies and equipment vendor quotation",
    "Vendor quotation price list supplier proposal cost estimate",
    "Contract agreement supplier terms conditions purchase agreement",
    "Delivery note goods received shipping invoice consignment",
    "Request for quotation RFQ tender procurement bid invitation",
    "Supplier invoice bill payment due vendor charges",
    "Purchase requisition approval needed items required buying",
    "Tender document bidding process procurement specifications",
    
    # Maintenance documents
    "Maintenance request for broken air conditioning system repair needed",
    "Repair work order facility maintenance schedule inspection",
    "Equipment maintenance log service record preventive maintenance",
    "Complaint regarding facility issues building problems reported",
    "Service report maintenance completed work done technician visit",
    "Inspection report building safety facility check findings",
    "Maintenance contract service agreement annual maintenance schedule",
    "Work completion certificate repair done maintenance finished",
]

labels = [
    'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
    'HR', 'HR', 'HR', 'HR', 'HR', 'HR', 'HR', 'HR',
    'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement',
    'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
]

print("Training document classifier...")
print(f"Training samples: {len(train_texts)}")
print(f"Categories: {set(labels)}")

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=1000,
    ngram_range=(1, 2),  # Use unigrams and bigrams
    min_df=1,
    stop_words='english'
)

# Transform texts
X = vectorizer.fit_transform(train_texts)
print(f"Feature dimensions: {X.shape}")

# Train LinearSVC classifier
classifier = LinearSVC(C=1.0, max_iter=1000)
classifier.fit(X, labels)

# Cross-validation score
scores = cross_val_score(classifier, X, labels, cv=3)
print(f"Cross-validation accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

# Save model
os.makedirs('models_store', exist_ok=True)
model_path = 'models_store/classifier.joblib'

joblib.dump({
    'vectorizer': vectorizer,
    'model': classifier,
    'categories': list(set(labels))
}, model_path)

print(f"Model saved to: {model_path}")

# Test predictions
print("\nTest predictions:")
test_texts = [
    "Invoice amount due payment required",
    "Employee leave request vacation",
    "Purchase order for supplies",
    "Repair broken equipment maintenance"
]

for text in test_texts:
    X_test = vectorizer.transform([text])
    prediction = classifier.predict(X_test)[0]
    print(f"  '{text[:40]}...' -> {prediction}")

print("\n✅ Classifier training complete!")
