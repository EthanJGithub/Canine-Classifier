"""
Image-based dog breed classifier using Hugging Face transformers.
Uses a pre-trained model to identify dog breeds from photos.
Cross-references results with local database for verification.
"""

import os
import sqlite3
from PIL import Image

# Import UI utilities
try:
    from ui_utils import (
        Colors, print_header, print_info, print_success, print_warning,
        print_error, print_divider, print_breed_result, loading_animation
    )
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    class Colors:
        RESET = BOLD = BRIGHT_WHITE = BRIGHT_CYAN = BRIGHT_YELLOW = ""
        BRIGHT_GREEN = BRIGHT_RED = DIM = BRIGHT_BLUE = BRIGHT_MAGENTA = ""


class DatabaseVerifier:
    """Verify AI predictions against local database."""

    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dog_database.db')
        self.db_breeds = set()
        self.breed_info = {}

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get all breeds from database
            cursor.execute("""
                SELECT BreedName, Size, CoatType, EarType, TailType
                FROM DogBreeds
            """)
            for row in cursor.fetchall():
                breed_name = row[0].lower()
                self.db_breeds.add(breed_name)
                self.breed_info[breed_name] = {
                    'size': row[1],
                    'coat': row[2],
                    'ears': row[3],
                    'tail': row[4]
                }

            conn.close()
        except Exception as e:
            print(f"Warning: Could not load database: {e}")

    def normalize_breed_name(self, breed):
        """Normalize breed name for comparison."""
        # Common mappings from ImageNet labels to database names
        mappings = {
            'golden retriever': 'golden retriever',
            'labrador retriever': 'labrador retriever',
            'german shepherd': 'german shepherd',
            'poodle': 'poodle',
            'standard poodle': 'poodle',
            'miniature poodle': 'poodle',
            'toy poodle': 'poodle',
            'siberian husky': 'siberian husky',
            'boxer': 'boxer',
            'rottweiler': 'rottweiler',
            'doberman': 'doberman pinscher',
            'doberman pinscher': 'doberman pinscher',
            'great dane': 'great dane',
            'chihuahua': 'chihuahua',
            'pomeranian': 'pomeranian',
            'shih-tzu': 'shih tzu',
            'shih tzu': 'shih tzu',
            'yorkshire terrier': 'yorkshire terrier',
            'pug': 'pug',
            'boston terrier': 'boston terrier',
            'border collie': 'border collie',
            'cocker spaniel': 'cocker spaniel',
            'english cocker spaniel': 'cocker spaniel',
            'saint bernard': 'saint bernard',
            'st. bernard': 'saint bernard',
            'shiba inu': 'shiba inu',
            'chow': 'chow chow',
            'chow chow': 'chow chow',
            'bernese mountain dog': 'bernese mountain dog',
            'maltese': 'maltese',
            'maltese dog': 'maltese',
            'cavalier king charles spaniel': 'cavalier king charles spaniel',
            'basset': 'basset hound',
            'basset hound': 'basset hound',
            'english setter': 'english setter',
            'australian shepherd': 'australian shepherd',
            'shetland sheepdog': 'shetland sheepdog',
            'dachshund': 'dachshund',
        }

        breed_lower = breed.lower().strip()
        return mappings.get(breed_lower, breed_lower)

    def verify_breed(self, breed_name):
        """Check if breed exists in database and return info."""
        normalized = self.normalize_breed_name(breed_name)

        if normalized in self.db_breeds:
            return {
                'verified': True,
                'db_name': normalized.title(),
                'info': self.breed_info.get(normalized, {})
            }

        # Try partial matching
        for db_breed in self.db_breeds:
            if db_breed in normalized or normalized in db_breed:
                return {
                    'verified': True,
                    'db_name': db_breed.title(),
                    'info': self.breed_info.get(db_breed, {})
                }

        return {'verified': False, 'db_name': None, 'info': {}}


class DogImageClassifier:
    def __init__(self):
        self.pipe = None
        self.model_loaded = False
        self.verifier = DatabaseVerifier()

    def load_model(self):
        """Lazy load the model to avoid slow startup when not using image mode."""
        if self.model_loaded:
            return True

        try:
            from transformers import pipeline
            if UI_AVAILABLE:
                print(f"  {Colors.BRIGHT_CYAN}⏳ Loading AI model (first run may take a moment)...{Colors.RESET}")
            else:
                print("Loading image recognition model (this may take a moment on first run)...")

            self.pipe = pipeline("image-classification", model="google/vit-base-patch16-224")
            self.model_loaded = True

            if UI_AVAILABLE:
                print(f"  {Colors.BRIGHT_GREEN}✓ Model loaded successfully!{Colors.RESET}")
            else:
                print("Model loaded successfully!")
            return True
        except Exception as e:
            if UI_AVAILABLE:
                print_error(f"Error loading model: {e}")
                print_info("Install required packages: pip install transformers torch torchvision Pillow")
            else:
                print(f"Error loading model: {e}")
            return False

    def classify_image(self, image_path: str, top_k: int = 5) -> list:
        """
        Classify a dog image and return predicted breeds with database verification.

        Args:
            image_path: Path to the dog image file
            top_k: Number of top predictions to return

        Returns:
            List of dicts with breed info, confidence, and verification status
        """
        if not self.load_model():
            return []

        if not os.path.exists(image_path):
            if UI_AVAILABLE:
                print_error(f"Image file not found: {image_path}")
            else:
                print(f"Error: Image file not found: {image_path}")
            return []

        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            if UI_AVAILABLE:
                loading_animation("Analyzing image", 0.5)

            results = self.pipe(image, top_k=top_k)

            # Process and verify results
            processed_results = []
            for result in results:
                label = result['label']
                score = result['score'] * 100

                # Clean up ImageNet labels
                if '_' in label:
                    label = label.replace('_', ' ').title()
                else:
                    label = label.title()

                # Verify against database
                verification = self.verifier.verify_breed(label)

                processed_results.append({
                    'breed': label,
                    'confidence': score,
                    'verified': verification['verified'],
                    'db_name': verification['db_name'],
                    'db_info': verification['info']
                })

            return processed_results

        except Exception as e:
            if UI_AVAILABLE:
                print_error(f"Error classifying image: {e}")
            else:
                print(f"Error classifying image: {e}")
            return []

    def display_results(self, results: list):
        """Display classification results with verification status."""
        if not results:
            if UI_AVAILABLE:
                print_warning("No results to display.")
            else:
                print("No results to display.")
            return

        # Check if any results are verified
        has_verified = any(r['verified'] for r in results)

        if UI_AVAILABLE:
            print()
            print_header("AI PREDICTION RESULTS", Colors.BRIGHT_GREEN)
            print()

            # Show verification status legend
            print(f"  {Colors.BRIGHT_GREEN}●{Colors.RESET} = In database (verified)    {Colors.BRIGHT_BLUE}○{Colors.RESET} = AI only (not in database)")
            print()
            print_divider()
            print()

            for i, result in enumerate(results, 1):
                breed = result['breed']
                confidence = result['confidence']
                verified = result['verified']
                db_info = result.get('db_info', {})

                # Status indicator
                if verified:
                    status = f"{Colors.BRIGHT_GREEN}●{Colors.RESET}"
                    breed_display = result.get('db_name', breed)
                else:
                    status = f"{Colors.BRIGHT_BLUE}○{Colors.RESET}"
                    breed_display = breed

                # Medal for top 3
                medals = {1: "🥇", 2: "🥈", 3: "🥉"}
                medal = medals.get(i, "  ")

                # Color based on confidence
                if confidence >= 80:
                    bar_color = Colors.BRIGHT_GREEN
                elif confidence >= 50:
                    bar_color = Colors.BRIGHT_YELLOW
                else:
                    bar_color = Colors.BRIGHT_RED

                # Build bar
                bar_width = 20
                filled = int(bar_width * confidence / 100)
                bar = "█" * filled + "░" * (bar_width - filled)

                print(f"  {medal} {status} {Colors.BOLD}{Colors.BRIGHT_WHITE}{breed_display:28}{Colors.RESET} {bar_color}[{bar}]{Colors.RESET} {Colors.BRIGHT_WHITE}{confidence:5.1f}%{Colors.RESET}")

                # Show database info if verified
                if verified and db_info:
                    info_parts = []
                    if db_info.get('size'):
                        info_parts.append(f"Size: {db_info['size']}")
                    if db_info.get('coat'):
                        info_parts.append(f"Coat: {db_info['coat']}")
                    if db_info.get('ears'):
                        info_parts.append(f"Ears: {db_info['ears']}")
                    if info_parts:
                        print(f"        {Colors.DIM}Database: {', '.join(info_parts)}{Colors.RESET}")

                print()

            print_divider()

            # Summary
            verified_count = sum(1 for r in results if r['verified'])
            if verified_count > 0:
                print_info(f"{verified_count} of {len(results)} predictions found in local database")
            else:
                print_warning("None of the predictions match breeds in local database")
                print_info("Results are based purely on AI computer vision")

            print_info("AI Model: Google Vision Transformer (ViT)")

        else:
            # Plain text output
            print("\n" + "=" * 50)
            print("IMAGE CLASSIFICATION RESULTS")
            print("=" * 50)
            print("\n● = In database    ○ = AI only\n")

            for i, result in enumerate(results, 1):
                breed = result['breed']
                confidence = result['confidence']
                verified = result['verified']

                status = "●" if verified else "○"
                breed_display = result.get('db_name', breed) if verified else breed

                bar_length = int(confidence / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)

                print(f"\n{i}. {status} {breed_display}")
                print(f"   Confidence: {confidence:.1f}%")
                print(f"   [{bar}]")

                if verified and result.get('db_info'):
                    info = result['db_info']
                    print(f"   Database: Size={info.get('size', 'N/A')}, Coat={info.get('coat', 'N/A')}")

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
