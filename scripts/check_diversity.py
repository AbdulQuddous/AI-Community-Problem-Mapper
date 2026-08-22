# scripts/check_diversity.py
"""
Quick diversity check for training data.
Run with: python scripts/check_diversity.py
"""
import os
import sys
from pathlib import Path
from collections import Counter

# Django setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.ai_engine.ml_data.training_data import TRAINING_EXAMPLES


def check_data_diversity(texts):
    print(f"\n📊 Total examples: {len(texts)}")
    
    # Check first-4-words prefix repetition
    prefixes = [" ".join(t.split()[:4]).lower() for t in texts]
    counts = Counter(prefixes)
    repeated = {p: c for p, c in counts.items() if c > 3}
    
    if repeated:
        print(f"\n⚠️  {len(repeated)} sentence openings repeated more than 3 times:")
        for prefix, count in sorted(repeated.items(), key=lambda x: -x[1])[:20]:
            print(f"   '{prefix}...' appears {count} times")
    else:
        print("\n✓ No obviously repetitive sentence patterns detected.")
    
    # Unique words
    all_words = set()
    for text in texts:
        for word in text.lower().split():
            all_words.add(word)
    
    print(f"\n📊 Unique words: {len(all_words)}")
    print(f"📊 Average words per complaint: {sum(len(t.split()) for t in texts) / len(texts):.1f}")
    
    # Category distribution
    from collections import Counter as CatCounter
    cat_counts = CatCounter([label for _, label in TRAINING_EXAMPLES])
    print("\n📊 Category distribution:")
    for cat, count in sorted(cat_counts.items()):
        print(f"   {cat}: {count}")


if __name__ == "__main__":
    texts = [text for text, _ in TRAINING_EXAMPLES]
    check_data_diversity(texts)