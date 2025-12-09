"""
Image-based dog breed classifier using Hugging Face transformers.
Uses a pre-trained model to identify dog breeds from photos.
"""

import os
from PIL import Image


class DogImageClassifier:
    def __init__(self):
        self.pipe = None
        self.model_loaded = False

    def load_model(self):
        """Lazy load the model to avoid slow startup when not using image mode."""
        if self.model_loaded:
            return True

        try:
            from transformers import pipeline
            print("Loading image recognition model (this may take a moment on first run)...")
            # Use a model trained on ImageNet which includes many dog breeds
            self.pipe = pipeline("image-classification", model="google/vit-base-patch16-224")
            self.model_loaded = True
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Make sure you have transformers and torch installed:")
            print("  pip install transformers torch torchvision Pillow")
            return False

    def classify_image(self, image_path: str, top_k: int = 5) -> list:
        """
        Classify a dog image and return predicted breeds.

        Args:
            image_path: Path to the dog image file
            top_k: Number of top predictions to return

        Returns:
            List of (breed, confidence) tuples
        """
        if not self.load_model():
            return []

        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return []

        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary (handles PNG with transparency, etc.)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            results = self.pipe(image, top_k=top_k)

            # Filter for dog-related predictions and clean up labels
            dog_results = []
            for result in results:
                label = result['label']
                score = result['score']
                # Clean up ImageNet labels (they often have format "n02099601 golden_retriever")
                if '_' in label:
                    label = label.replace('_', ' ').title()
                dog_results.append((label, score * 100))

            return dog_results

        except Exception as e:
            print(f"Error classifying image: {e}")
            return []

    def display_results(self, results: list):
        """Display classification results in a formatted way."""
        if not results:
            print("No results to display.")
            return

        print("\n" + "=" * 50)
        print("IMAGE CLASSIFICATION RESULTS")
        print("=" * 50)

        for i, (breed, confidence) in enumerate(results, 1):
            bar_length = int(confidence / 2)  # Scale to max 50 chars
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"\n{i}. {breed}")
            print(f"   Confidence: {confidence:.1f}%")
            print(f"   [{bar}]")

        print("\n" + "=" * 50)


def classify_dog_image(image_path: str):
    """Convenience function to classify a dog image."""
    classifier = DogImageClassifier()
    results = classifier.classify_image(image_path)
    classifier.display_results(results)
    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        classify_dog_image(image_path)
    else:
        print("Usage: python image_classifier.py <path_to_dog_image>")
        print("Example: python image_classifier.py my_dog.jpg")
