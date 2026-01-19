"""
Enhanced Document Classifier with Better Accuracy
Features:
- Ensemble methods (Random Forest + SVM)
- Better feature extraction
- Detailed model metrics and analysis
- Confidence scores and probability distributions
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import numpy as np
import joblib
import os
from datetime import datetime

# Enhanced training data with more diverse examples
train_texts = [
    # Finance documents (25 examples)
    "Invoice for payment of services rendered Amount due 5000 rupees quarterly billing",
    "Financial statement quarterly report revenue expenses profit loss balance sheet",
    "Receipt for purchase payment confirmation transaction completed invoice number",
    "Budget proposal financial planning annual expenses allocation department budgets",
    "Tax document income tax filing annual return financial year deduction",
    "Bank statement account balance transactions deposits withdrawals statement date",
    "Expense report reimbursement travel costs business expenses mileage hotel",
    "Payment voucher cash disbursement approved amount paid authorization",
    "Audit report financial audit compliance verification internal controls assessment",
    "Purchase invoice supplier bill amount due payment terms net",
    "Credit memo adjustment deduction refund previous invoice correction",
    "Petty cash report small expenses miscellaneous spending documentation",
    "Monthly accounting summary revenue analysis cost breakdown profit",
    "Financial forecast projection revenue estimate expense budget planning",
    "Payroll summary salary calculation deductions tax withholding net pay",
    "Invoice tracking aging report payment status overdue accounts",
    "Transfer voucher fund transfer between accounts document verification",
    "Ledger entry transaction posting debit credit account statement",
    "Financial ratio analysis performance metrics profitability liquidity solvency",
    "Cost allocation expense distribution departmental budget tracking",
    "Fixed asset depreciation schedule equipment valuation book value",
    "Accrual entry transaction posting revenue recognition expense matching",
    "Bank reconciliation statement clearing outstanding checks deposits",
    "Treasury management cash position liquidity forecast reserve",
    "Capital expenditure authorization asset purchase investment approval",
    
    # HR documents (25 examples)
    "Employee leave application vacation days annual leave approval request",
    "Resignation letter notice period last working day employment termination",
    "Job offer letter employment contract salary position appointment offer",
    "Performance appraisal employee evaluation annual review rating feedback",
    "Attendance record working hours time sheet employee presence log",
    "Training certificate course completion employee development program credential",
    "Salary slip payslip monthly wages deductions tax net pay",
    "Employee handbook company policies code of conduct rules guidelines",
    "Promotion letter career advancement position upgrade salary increase",
    "Transfer request department change relocation employee movement",
    "Disciplinary action warning letter code violation misconduct",
    "Termination letter employment end severance final paycheck",
    "Medical leave sick leave health absence medical certificate",
    "Maternity leave paternity leave parental leave family benefit",
    "Bereavement leave compassionate leave family emergency leave",
    "Educational leave study leave sponsorship employee development",
    "Sick leave medical certificate health issue absence authorization",
    "Annual leave planning vacation scheduling time off request",
    "Overtime approval extra hours authorization compensation pay",
    "Bonus allocation incentive payment performance reward recognition",
    "Performance improvement plan employee development remedial action",
    "Background verification check candidate screening employment verification",
    "Induction checklist onboarding process new employee orientation",
    "Competency assessment skill evaluation employee capability rating",
    "Career development plan growth strategy promotion pathway planning",
    
    # Procurement documents (25 examples)
    "Purchase order for office supplies and equipment vendor quotation",
    "Vendor quotation price list supplier proposal cost estimate rate",
    "Contract agreement supplier terms conditions purchase agreement",
    "Delivery note goods received shipping invoice consignment details",
    "Request for quotation RFQ tender procurement bid invitation",
    "Supplier invoice bill payment due vendor charges amount",
    "Purchase requisition approval needed items required buying request",
    "Tender document bidding process procurement specifications requirements",
    "Goods receipt verification inspection quality check acceptance",
    "Bill of lading shipping document freight carrier receipt",
    "Packing slip item list quantity contents shipment details",
    "Customs clearance import document duty payment tariff",
    "Purchase agreement contract supplier terms payment conditions",
    "Three way match purchase order invoice receipt verification",
    "Vendor performance evaluation supplier rating feedback assessment",
    "Purchase authorization approval amount limit budget allocated",
    "Bulk order discount agreement volume purchase terms negotiated",
    "Return authorization RMA defect replacement refund processing",
    "Supplier agreement framework contract volume commitment terms",
    "Purchase history vendor transactions previous orders summary",
    "Service contract maintenance agreement vendor support terms",
    "Price agreement fixed rate contract negotiated terms pricing",
    "Logistics coordination shipping arrangement delivery scheduling",
    "Inventory adjustment stock movement purchase receipt adjustment",
    "Procurement request emergency purchase expedited order urgent",
    
    # Maintenance documents (25 examples)
    "Maintenance request for broken air conditioning system repair needed",
    "Repair work order facility maintenance schedule inspection required",
    "Equipment maintenance log service record preventive maintenance history",
    "Complaint regarding facility issues building problems reported repair",
    "Service report maintenance completed work done technician visit",
    "Inspection report building safety facility check findings assessment",
    "Maintenance contract service agreement annual maintenance schedule terms",
    "Work completion certificate repair done maintenance finished verified",
    "Preventive maintenance plan schedule equipment service dates",
    "Equipment breakdown report failure analysis root cause investigation",
    "Maintenance budget allocation resource planning maintenance expense",
    "Technician report field visit observations repairs completed",
    "Safety inspection checklist compliance verification hazard assessment",
    "Facility assessment evaluation condition status recommendations",
    "Maintenance ticket urgent request immediate attention priority",
    "Equipment warranty coverage service included support duration",
    "Spare parts inventory stock supply maintenance material",
    "Maintenance cost analysis expense tracking service efficiency",
    "Facility upgrade plan improvement authorization renovation",
    "Scheduled maintenance calendar preventive service dates timing",
    "Emergency repair authorization breakdown urgent action immediate",
    "Quality check maintenance verification workmanship inspection",
    "Equipment relocation moving service facility change",
    "Cleaning schedule housekeeping janitorial service plan",
    "Environmental safety compliance inspection regulatory requirements",
]

labels = [
    # Finance (25)
    'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
    'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
    'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
    'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
    'Finance', 'Finance', 'Finance', 'Finance', 'Finance',
    # HR (25)
    'HR', 'HR', 'HR', 'HR', 'HR',
    'HR', 'HR', 'HR', 'HR', 'HR',
    'HR', 'HR', 'HR', 'HR', 'HR',
    'HR', 'HR', 'HR', 'HR', 'HR',
    'HR', 'HR', 'HR', 'HR', 'HR',
    # Procurement (25)
    'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement',
    'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement',
    'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement',
    'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement',
    'Procurement', 'Procurement', 'Procurement', 'Procurement', 'Procurement',
    # Maintenance (25)
    'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
    'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
    'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
    'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
    'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance', 'Maintenance',
]

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"📊 {title}")
    print("="*80)

def print_subsection(title):
    """Print formatted subsection"""
    print(f"\n{'─'*80}\n📈 {title}\n{'─'*80}")

# =============================================================================
# STEP 1: DATA PREPARATION
# =============================================================================
print_section("STEP 1: DATA PREPARATION")

print(f"\n✓ Total training samples: {len(train_texts)}")
print(f"✓ Number of categories: {len(set(labels))}")

category_distribution = {}
for label in labels:
    category_distribution[label] = category_distribution.get(label, 0) + 1

print("\n📋 Category Distribution:")
for category, count in sorted(category_distribution.items()):
    percentage = (count / len(labels)) * 100
    bar_length = int(percentage / 2)
    bar = '█' * bar_length + '░' * (50 - bar_length)
    print(f"  {category:15} {count:3} samples ({percentage:5.1f}%) {bar}")

# Split data for testing
X_train_text, X_test_text, y_train, y_test = train_test_split(
    train_texts, labels, test_size=0.2, random_state=42, stratify=labels
)

print(f"\n✓ Training set size: {len(X_train_text)}")
print(f"✓ Test set size: {len(X_test_text)}")

# =============================================================================
# STEP 2: FEATURE EXTRACTION - TF-IDF
# =============================================================================
print_section("STEP 2: FEATURE EXTRACTION")

# TF-IDF Vectorizer with optimized parameters
vectorizer = TfidfVectorizer(
    max_features=500,        # Reduced to focus on important features
    ngram_range=(1, 3),      # Include trigrams
    min_df=1,                # Minimum document frequency
    max_df=0.9,              # Maximum document frequency
    sublinear_tf=True,       # Apply sublinear term frequency scaling
    strip_accents='unicode',
    lowercase=True,
    analyzer='word',
    token_pattern=r'\w{1,}',
    stop_words='english'
)

X_train_tfidf = vectorizer.fit_transform(X_train_text)
X_test_tfidf = vectorizer.transform(X_test_text)

print(f"\n✓ TF-IDF Feature Matrix Shape: {X_train_tfidf.shape}")
print(f"✓ Vocabulary size: {len(vectorizer.get_feature_names_out())}")
print(f"✓ Sparsity: {1.0 - (X_train_tfidf.nnz / (X_train_tfidf.shape[0] * X_train_tfidf.shape[1]))*100:.1f}%")

# Show top features
feature_names = vectorizer.get_feature_names_out()
print(f"\n✓ Sample features (first 20): {', '.join(feature_names[:20])}")

# =============================================================================
# STEP 3: MODEL TRAINING - ENSEMBLE APPROACH
# =============================================================================
print_section("STEP 3: MODEL TRAINING (ENSEMBLE)")

# Model 1: Logistic Regression (has predict_proba)
print("\n📍 Training Model 1: LogisticRegression...")
lr_model = LogisticRegression(
    max_iter=2000,
    random_state=42,
    class_weight='balanced',
    solver='lbfgs'
)
lr_model.fit(X_train_tfidf, y_train)
lr_train_score = lr_model.score(X_train_tfidf, y_train)
lr_test_score = lr_model.score(X_test_tfidf, y_test)
print(f"   ✓ LogisticRegression Training Accuracy: {lr_train_score*100:.2f}%")
print(f"   ✓ LogisticRegression Test Accuracy: {lr_test_score*100:.2f}%")

# Model 2: Random Forest with TF-IDF
print("\n📍 Training Model 2: RandomForest...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
rf_model.fit(X_train_tfidf, y_train)
rf_train_score = rf_model.score(X_train_tfidf, y_train)
rf_test_score = rf_model.score(X_test_tfidf, y_test)
print(f"   ✓ RandomForest Training Accuracy: {rf_train_score*100:.2f}%")
print(f"   ✓ RandomForest Test Accuracy: {rf_test_score*100:.2f}%")

# Ensemble Model
print("\n📍 Training Ensemble Model (Voting Classifier)...")
ensemble_model = VotingClassifier(
    estimators=[
        ('lr', lr_model),
        ('rf', rf_model)
    ],
    voting='soft'
)
ensemble_model.fit(X_train_tfidf, y_train)
ensemble_train_score = ensemble_model.score(X_train_tfidf, y_train)
ensemble_test_score = ensemble_model.score(X_test_tfidf, y_test)
print(f"   ✓ Ensemble Training Accuracy: {ensemble_train_score*100:.2f}%")
print(f"   ✓ Ensemble Test Accuracy: {ensemble_test_score*100:.2f}%")

# Model 1: Linear SVC
print("\n📍 Training Model 1: LinearSVC...")
svm_model = LinearSVC(
    C=0.5,
    max_iter=2000,
    dual=False,
    random_state=42,
    class_weight='balanced'
)
svm_model.fit(X_train_tfidf, y_train)
svm_train_score = svm_model.score(X_train_tfidf, y_train)
svm_test_score = svm_model.score(X_test_tfidf, y_test)
print(f"   ✓ LinearSVC Training Accuracy: {svm_train_score*100:.2f}%")
print(f"   ✓ LinearSVC Test Accuracy: {svm_test_score*100:.2f}%")

# =============================================================================
# STEP 4: CROSS-VALIDATION
# =============================================================================
print_section("STEP 4: CROSS-VALIDATION ANALYSIS")

print("\n📊 5-Fold Cross-Validation Scores:")
cv_scores = cross_val_score(ensemble_model, X_train_tfidf, y_train, cv=5, scoring='accuracy')
print(f"   Fold 1: {cv_scores[0]*100:.2f}%")
print(f"   Fold 2: {cv_scores[1]*100:.2f}%")
print(f"   Fold 3: {cv_scores[2]*100:.2f}%")
print(f"   Fold 4: {cv_scores[3]*100:.2f}%")
print(f"   Fold 5: {cv_scores[4]*100:.2f}%")
print(f"\n   Mean Accuracy: {cv_scores.mean()*100:.2f}% (±{cv_scores.std()*100:.2f}%)")

# =============================================================================
# STEP 5: DETAILED CLASSIFICATION REPORT
# =============================================================================
print_section("STEP 5: DETAILED CLASSIFICATION METRICS")

y_pred = ensemble_model.predict(X_test_tfidf)

# Classification Report
print_subsection("CLASSIFICATION REPORT (TEST SET)")
print("\n" + classification_report(y_test, y_pred, digits=4))

# Precision, Recall, F1 per class
print_subsection("PER-CLASS DETAILED METRICS")
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
categories = sorted(set(labels))

print(f"\n{'Category':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
print("─" * 70)
for i, category in enumerate(categories):
    print(f"{category:<15} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]:<10}")

# Confusion Matrix
print_subsection("CONFUSION MATRIX (TEST SET)")
cm = confusion_matrix(y_test, y_pred)
print(f"\n{'':15}", end='')
for cat in categories:
    print(f"{cat:>12}", end='')
print()
print("─" * (15 + len(categories) * 12))
for i, cat in enumerate(categories):
    print(f"{cat:<15}", end='')
    for j in range(len(categories)):
        print(f"{cm[i, j]:>12}", end='')
    print()

# =============================================================================
# STEP 6: FEATURE IMPORTANCE
# =============================================================================
print_section("STEP 6: FEATURE IMPORTANCE ANALYSIS")

# Get feature importance from Random Forest
rf_importance = rf_model.feature_importances_
top_features_idx = np.argsort(rf_importance)[-20:][::-1]

print_subsection("TOP 20 MOST IMPORTANT FEATURES")
for idx, feature_idx in enumerate(top_features_idx, 1):
    feature_name = feature_names[feature_idx]
    importance_score = rf_importance[feature_idx]
    bar_length = int(importance_score * 50)
    bar = '█' * bar_length
    print(f"{idx:2}. {feature_name:20} {importance_score:6.4f} {bar}")

# =============================================================================
# STEP 7: TEST PREDICTIONS WITH CONFIDENCE
# =============================================================================
print_section("STEP 7: TEST PREDICTIONS WITH CONFIDENCE SCORES")

test_samples = [
    "Invoice for payment of services Amount due 5000",
    "Employee leave request vacation days approved",
    "Purchase order office supplies vendor quotation",
    "Equipment maintenance repair air conditioning system",
    "Financial statement quarterly revenue report",
    "Job offer letter employment contract salary position",
]

print_subsection("SAMPLE PREDICTIONS WITH DETAILED ANALYSIS")

for i, sample_text in enumerate(test_samples, 1):
    # Vectorize
    sample_vec = vectorizer.transform([sample_text])
    
    # Get prediction from each model
    svm_pred = svm_model.predict(sample_vec)[0]
    rf_pred = rf_model.predict(sample_vec)[0]
    ensemble_pred = ensemble_model.predict(sample_vec)[0]
    
    # Get probability estimates
    rf_proba = rf_model.predict_proba(sample_vec)[0]
    
    print(f"\n{i}. Sample: \"{sample_text}\"")
    print(f"   {'─'*70}")
    print(f"   SVM Prediction:      {svm_pred}")
    print(f"   Random Forest:       {rf_pred}")
    print(f"   Ensemble Prediction: {ensemble_pred}")
    
    print(f"\n   Probability Distribution:")
    for j, category in enumerate(categories):
        prob = rf_proba[j]
        bar_length = int(prob * 40)
        bar = '█' * bar_length + '░' * (40 - bar_length)
        print(f"      {category:15} {prob*100:6.2f}% {bar}")

# =============================================================================
# STEP 8: SAVE MODELS
# =============================================================================
print_section("STEP 8: SAVING ENHANCED MODEL")

os.makedirs('models_store', exist_ok=True)

# Save ensemble model
model_path = 'models_store/enhanced_classifier.joblib'
joblib.dump({
    'vectorizer': vectorizer,
    'ensemble_model': ensemble_model,
    'lr_model': lr_model,
    'rf_model': rf_model,
    'svm_model': svm_model,
    'categories': categories,
    'feature_names': feature_names,
    'training_accuracy': ensemble_train_score,
    'test_accuracy': ensemble_test_score,
    'cross_val_mean': cv_scores.mean(),
    'cross_val_std': cv_scores.std(),
    'trained_at': datetime.now().isoformat(),
}, model_path)

print(f"\n✅ Enhanced model saved to: {model_path}")

# Save metrics report
metrics_path = 'models_store/model_metrics.txt'
with open(metrics_path, 'w') as f:
    f.write("ENHANCED DOCUMENT CLASSIFIER - METRICS REPORT\n")
    f.write(f"{'='*80}\n")
    f.write(f"Trained at: {datetime.now().isoformat()}\n\n")
    
    f.write(f"ACCURACY SCORES:\n")
    f.write(f"  Training: {ensemble_train_score*100:.2f}%\n")
    f.write(f"  Test:     {ensemble_test_score*100:.2f}%\n")
    f.write(f"  Cross-Val Mean: {cv_scores.mean()*100:.2f}%\n")
    f.write(f"  Cross-Val Std:  {cv_scores.std()*100:.2f}%\n\n")
    
    f.write(f"CLASSIFICATION REPORT:\n")
    f.write(classification_report(y_test, y_pred, digits=4))

print(f"✅ Metrics report saved to: {metrics_path}")

# =============================================================================
# SUMMARY
# =============================================================================
print_section("SUMMARY")
print(f"""
✅ Enhanced Classifier Training Complete!

📊 Model Performance:
   • Ensemble Accuracy:        {ensemble_test_score*100:.2f}%
   • Cross-Validation Score:   {cv_scores.mean()*100:.2f}% (±{cv_scores.std()*100:.2f}%)
   • Training Set Size:        {len(X_train_text)} samples
   • Test Set Size:            {len(X_test_text)} samples

🔧 Model Architecture:
   • Feature Extraction:       TF-IDF (500 features, n-grams: 1-3)
   • Algorithm 1:              LinearSVC (C=0.5)
   • Algorithm 2:              RandomForest (100 trees)
   • Ensemble Method:          Soft Voting Classifier

📁 Files Saved:
   ✓ {model_path}
   ✓ {metrics_path}

🎯 Categories:
   {', '.join(categories)}

""")

print("="*80)
print("✨ Ready to use in flask_documents_api.py!")
print("="*80)
