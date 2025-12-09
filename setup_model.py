#!/usr/bin/env python3
"""
Model Setup Script for Canine Classifier
Downloads and saves the AI model locally for offline use.
Run this once after cloning the repository.
"""

import os
import sys

def setup_model():
    """Download and save the Vision Transformer model locally."""

    print("=" * 60)
    print("  CANINE CLASSIFIER - AI MODEL SETUP")
    print("=" * 60)
    print()

    # Check if model already exists
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'vit-dog-classifier')

    if os.path.exists(model_dir) and os.path.exists(os.path.join(model_dir, 'model.safetensors')):
        print("  [OK] Model already downloaded!")
        print(f"  Location: {model_dir}")
        print()
        print("  You can now run: python ElizaGUI.py")
        return True

    print("  Downloading Vision Transformer model...")
    print("  This is a one-time download (~350MB)")
    print()

    try:
        from transformers import ViTForImageClassification, ViTImageProcessor

        print("  [1/3] Downloading model weights...")
        model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

        print("  [2/3] Downloading image processor...")
        processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')

        print("  [3/3] Saving model locally...")
        os.makedirs(model_dir, exist_ok=True)
        model.save_pretrained(model_dir)
        processor.save_pretrained(model_dir)

        print()
        print("  [OK] Model downloaded successfully!")
        print(f"  Location: {model_dir}")
        print()
        print("=" * 60)
        print("  SETUP COMPLETE!")
        print("  You can now run: python ElizaGUI.py")
        print("=" * 60)

        return True

    except ImportError:
        print()
        print("  [ERROR] Required packages not installed!")
        print()
        print("  Please run:")
        print("    pip install transformers torch torchvision Pillow")
        print()
        print("  Then run this script again:")
        print("    python setup_model.py")
        return False

    except Exception as e:
        print()
        print(f"  [ERROR] Failed to download model: {e}")
        print()
        print("  Make sure you have an internet connection and try again.")
        return False


if __name__ == "__main__":
    success = setup_model()
    sys.exit(0 if success else 1)
