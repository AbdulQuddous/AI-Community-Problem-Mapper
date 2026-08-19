"""
Trains the local complaint classifier and saves it to
apps/ai_engine/ml_models/classifier.joblib.

Usage (from project root, with venv activated):
    python scripts/train_classifier.py

Pipeline:
    1. Load labeled examples from apps.ai_engine.ml_data.training_data
    2. Generate a Sentence Transformer embedding for each example text
       (reuses embedding_service.py — same model used at inference
       time, so training and serving embeddings are guaranteed
       consistent).
    3. Fit a LogisticRegression classifier on (embedding -> category).
    4. Save the fitted classifier + label encoder together as one
       joblib bundle, so local_classifier_service.py has no separate
       label-mapping file to keep in sync.
    5. Print a held-out accuracy estimate, per-category report, and a
       confusion matrix so you can see exactly which categories are
       being confused with which before relying on this in production.

Re-run this script any time apps/ai_engine/ml_data/training_data.py
is extended with more labeled examples.
"""
import os
import sys
from pathlib import Path
from collections import Counter

import django

# --- Django setup, since embedding_service.py needs settings.py ---
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import joblib  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold  # noqa: E402
from sklearn.preprocessing import LabelEncoder  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from apps.ai_engine.ml_data.training_data import TRAINING_EXAMPLES  # noqa: E402
from apps.ai_engine.services.embedding_service import generate_embedding  # noqa: E402
from django.conf import settings  # noqa: E402


def check_data_diversity(texts: list[str]) -> None:
    """
    Flags suspiciously repetitive training data — a common cause of
    misleadingly perfect held-out accuracy when data is LLM-generated
    in batches, since near-duplicate phrasing can leak the 'answer'
    across the train/test split.
    """
    # Check first-4-words prefix repetition
    prefixes = [" ".join(t.split()[:4]).lower() for t in texts]
    counts = Counter(prefixes)
    repeated = {p: c for p, c in counts.items() if c > 3}
    
    if repeated:
        print(f"\n⚠️  {len(repeated)} sentence openings repeated more than 3 times:")
        for prefix, count in sorted(repeated.items(), key=lambda x: -x[1])[:15]:
            print(f"   '{prefix}...' appears {count} times")
    else:
        print("\n✓ No obviously repetitive sentence patterns detected.")
    
    # Check unique words
    all_words = set()
    for text in texts:
        for word in text.lower().split():
            all_words.add(word)
    print(f"\n📊 Unique words in dataset: {len(all_words)}")
    print(f"📊 Average words per complaint: {sum(len(t.split()) for t in texts) / len(texts):.1f}")
    print(f"📊 Total examples: {len(texts)}")


def print_confusion_matrix(y_true, y_pred, class_names) -> None:
    """
    Prints a readable confusion matrix: rows = true category,
    columns = predicted category. Diagonal = correct predictions;
    off-diagonal cells show exactly which categories are being
    confused with which, so dataset improvements can target the
    actual overlap instead of guessing.
    """
    matrix = confusion_matrix(y_true, y_pred)
    col_width = max(len(name) for name in class_names) + 2

    print("\nConfusion Matrix (rows = actual, columns = predicted):")
    header = " " * col_width + "".join(f"{name[:8]:>10}" for name in class_names)
    print(header)
    for i, row_name in enumerate(class_names):
        row_str = f"{row_name:<{col_width}}" + "".join(f"{matrix[i][j]:>10}" for j in range(len(class_names)))
        print(row_str)

    # Highlight the actual confusions (off-diagonal, non-zero) as a
    # plain-English list — easier to scan than the grid above.
    print("\nMisclassifications (actual -> predicted: count):")
    found_any = False
    for i, true_name in enumerate(class_names):
        for j, pred_name in enumerate(class_names):
            if i != j and matrix[i][j] > 0:
                print(f"  {true_name} -> {pred_name}: {matrix[i][j]}")
                found_any = True
    if not found_any:
        print("  None — perfect classification on the held-out set.")


def main() -> None:
    print(f"Loading {len(TRAINING_EXAMPLES)} labeled training examples...")
    texts = [text for text, _ in TRAINING_EXAMPLES]
    labels = [label for _, label in TRAINING_EXAMPLES]

    # --- Diversity Check ---
    check_data_diversity(texts)

    print("\nGenerating embeddings (this loads the Sentence Transformer model)...")
    embeddings = [generate_embedding(text) for text in texts]

    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)

    # --- Cross-Validation (More reliable than single split) ---
    print("\n📊 Running 5-fold cross-validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(
        LogisticRegression(max_iter=1000, C=0.1, random_state=42),
        embeddings,
        encoded_labels,
        cv=cv,
        scoring='accuracy'
    )
    print(f"   5-fold CV accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")

    # --- Single train/test split (for detailed reporting) ---
    x_train, x_test, y_train, y_test = train_test_split(
        embeddings, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels,
    )

    print(f"\nTraining LogisticRegression on {len(x_train)} examples...")
    # C=0.1 = stronger regularization to prevent overfitting
    classifier = LogisticRegression(max_iter=1000, C=0.1, random_state=42)
    classifier.fit(x_train, y_train)

    y_pred = classifier.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nHeld-out accuracy: {accuracy:.2%}")

    print("\nPer-category performance:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_, zero_division=0))

    print_confusion_matrix(y_test, y_pred, label_encoder.classes_)

    # Refit on ALL data (train + test) before saving, so the shipped
    # model benefits from every labeled example, not just the 80% split
    # used for evaluation above.
    print("\nRefitting on full dataset for the final saved model...")
    classifier.fit(embeddings, encoded_labels)

    model_path = Path(settings.LOCAL_CLASSIFIER_MODEL_PATH)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"classifier": classifier, "label_encoder": label_encoder}, model_path)
    print(f"\nModel saved to {model_path}")


if __name__ == "__main__":
    main()