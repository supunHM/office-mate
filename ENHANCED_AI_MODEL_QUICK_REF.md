# Enhanced AI Model - Quick Reference Guide

## 🚀 Quick Start

### Train the Enhanced Model (First Time)

```bash
cd /Users/supunherath/Documents/Dev-Pro/office-mate-backend
source ../.venv/bin/activate
python train_enhanced_classifier.py
```

**What happens:**
- Trains ensemble model (Logistic Regression + Random Forest)
- Generates detailed metrics report
- Saves model and evaluation results
- Shows sample predictions with confidence

---

## 📊 Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **Accuracy** | 63% | 75% |
| **Algorithms** | 1 (Linear SVC) | 2 (Logistic + RF) |
| **Confidence Scores** | ❌ None | ✅ Yes (detailed) |
| **Feature Analysis** | ❌ None | ✅ Top 20 keywords |
| **Model Agreement** | ❌ None | ✅ Consensus checking |
| **Probability Distribution** | ❌ None | ✅ All categories |

---

## 📈 Classification Response Format

When you upload a document, it returns:

```json
{
  "id": 1,
  "category": "Finance",
  "tags": ["invoice", "payment"],
  "filename": "invoice.pdf",
  "classification_details": {
    "confidence": "55.52%",
    "confidence_level": "Medium",
    "model_agreement": true,
    "agreement_strength": "High",
    "top_features": ["financial", "statement", "revenue", "quarterly", "report"],
    "probability_ranking": [
      ["Finance", 0.5552],
      ["Maintenance", 0.1964],
      ["HR", 0.1309],
      ["Procurement", 0.1175]
    ],
    "analysis": "✓ Document classified as Finance | ✓ Good confidence (55.5%) | ✓ All models agree"
  }
}
```

---

## 🎯 Confidence Levels

**Use this table to decide if classification is reliable:**

| Level | Score | Action |
|-------|-------|--------|
| Very High | 85%+ | ✅ Auto-approve, safe for automation |
| High | 70-85% | ✅ Approve with confidence |
| Medium | 55-70% | ⚠️ Review recommended |
| Low | 40-55% | ⚠️ Manual review suggested |
| Very Low | <40% | ❌ Requires manual classification |

---

## 🔑 Understanding Top Features

**Top features are the keywords that influenced the prediction:**

Example for Finance document:
```
Top Features: 
1. financial (weight: 0.456)
2. statement (weight: 0.389)
3. revenue (weight: 0.367)
4. quarterly (weight: 0.312)
5. report (weight: 0.298)
```

**What this means:**
- Words like "financial", "statement" strongly indicate Finance
- Higher weights = stronger influence on classification
- Features help validate if prediction makes sense

---

## 🤖 Model Agreement Explained

**All models check if different algorithms agree:**

```
SVM says:           Finance  ○
Random Forest says: Finance  ○
Ensemble predicts:  Finance  ✓
All agree?          YES ✓
```

**Why this matters:**
- If all models agree → High confidence
- If they disagree → Lower confidence
- Helps catch questionable classifications

---

## 📊 Model Performance Metrics

### Training Results

```
Total Training Samples: 100
- Finance:      25 samples (25%)
- HR:           25 samples (25%)
- Procurement:  25 samples (25%)
- Maintenance:  25 samples (25%)

Test Accuracy:           75.00%
Cross-Validation Score:  78.75% (±8.48%)
```

### Per-Category Accuracy

| Category | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Finance | 57% | 80% | 67% |
| HR | 80% | 80% | 80% |
| Maintenance | 83% | 100% | 91% |
| Procurement | 100% | 40% | 57% |

---

## 💻 Using the Enhanced Classifier in Code

### Python API

```python
from enhanced_classifier import classify_document_enhanced

# Classify a document
result = classify_document_enhanced(text)

# Access results
print(f"Category: {result['predicted_category']}")
print(f"Confidence: {result['confidence_percentage']}")
print(f"Level: {result['confidence_level']}")
print(f"Top Features: {result['top_features'][:5]}")
print(f"All Agree?: {result['models_agree']}")
```

### Flask API

```bash
# Upload document (automatic classification)
curl -X POST http://localhost:8000/api/documents \
  -F "file=@document.pdf"

# Response includes classification_details
```

---

## 🎓 Key Concepts

### Confidence Score (0.0 - 1.0)
- How certain the model is about its prediction
- 0.5552 = 55.52% confident
- Calculated from probability distribution

### Probability Distribution
- Score for each category
- Sum of all scores = 1.0
- Example: Finance=0.55, HR=0.13, Maintenance=0.20, Procurement=0.12

### Top Features
- Keywords most important for this prediction
- Listed in order of importance (weight)
- Use to verify prediction makes sense

### Model Agreement
- Multiple algorithms vote on the classification
- If consensus exists, confidence is higher
- Disagreement may indicate ambiguous document

### Feature Importance
- Shows which keywords the model learned as indicators
- "Employee" = strongest HR indicator
- "Purchase" = strongest Procurement indicator

---

## 📁 Files & Locations

**Model Files:**
- `models_store/enhanced_classifier.joblib` - Saved ensemble model
- `models_store/model_metrics.txt` - Performance metrics

**Code Files:**
- `train_enhanced_classifier.py` - Training script
- `enhanced_classifier.py` - Classification module
- `flask_documents_api.py` - API integration

**Documentation:**
- `ENHANCED_AI_MODEL.md` - Full documentation (this file)
- `ENHANCED_AI_MODEL_QUICK_REF.md` - This quick reference

---

## 🔄 Workflow Example

### Uploading a Document

```
1. User uploads invoice.pdf
   ↓
2. Backend extracts text (OCR/PDF extraction)
   ↓
3. Enhanced classifier analyzes:
   - Vectorizes text to 500 TF-IDF features
   - Logistic Regression predicts: Finance
   - Random Forest predicts: Finance
   - Ensemble votes: Finance (confident)
   ↓
4. Returns response with:
   - Category: Finance
   - Confidence: 55.52% (Medium)
   - Top features: [financial, statement, revenue]
   - Model agreement: ✓ All agree
   ↓
5. API Response sent to frontend
   with full classification details
```

---

## ⚙️ Configuration

### Model Parameters

**TF-IDF Features:**
```python
max_features=500          # Focus on top 500 words
ngram_range=(1, 3)        # Use single/double/triple words
sublinear_tf=True         # Better feature scaling
```

**Logistic Regression:**
```python
max_iter=2000             # Iterations for convergence
solver='lbfgs'            # Optimization algorithm
class_weight='balanced'   # Handle imbalanced categories
```

**Random Forest:**
```python
n_estimators=100          # 100 decision trees
max_depth=15              # Max tree depth
min_samples_split=5       # Min samples to split
```

---

## 🔍 Troubleshooting

### Model Not Found Error

```
Error: enhanced_classifier.joblib not found

Solution:
  python train_enhanced_classifier.py
```

### Low Confidence on New Documents

**Possible causes:**
- Document is truly ambiguous
- Text is very short
- Contains mix of different document types
- Keywords are new/unseen in training

**Solution:**
- Provide manual classification
- Add document to training data
- Retrain model with updated samples

### Models Disagree

**What it means:**
- Different algorithms see different signals
- Document is hard to classify
- May have mixed characteristics

**Recommendation:**
- Manual review suggested
- Check top_features to understand why
- Consider if it's a hybrid document

---

## 📞 Quick Help

### Check Model Status
```bash
cd office-mate-backend
python -c "from enhanced_classifier import EnhancedClassifier; 
           c = EnhancedClassifier(); 
           print('✓ Enhanced classifier loaded successfully')"
```

### View Metrics
```bash
cat models_store/model_metrics.txt
```

### Test Classifier
```bash
python enhanced_classifier.py
```

### Retrain Model
```bash
python train_enhanced_classifier.py
```

---

## 📚 Learn More

**Full Documentation:** See `ENHANCED_AI_MODEL.md`

**Categories Supported:**
- Finance (invoices, receipts, budgets, reports)
- HR (leave, contracts, payroll, reviews)
- Procurement (purchase orders, quotations, contracts)
- Maintenance (repairs, inspections, work orders)

**Model Type:**
- Ensemble: Soft Voting Classifier
- Algorithms: Logistic Regression + Random Forest
- Features: TF-IDF with n-grams (1-3)
- Accuracy: 75% on test set

---

## ✨ Summary

The enhanced AI model provides:
- **75% Accuracy** with ensemble voting
- **Detailed Confidence Scores** (5 levels)
- **Top Features** showing prediction reasons
- **Model Agreement** checking for consensus
- **Probability Distribution** of all categories

Use it to make smart, automated document classification decisions!
