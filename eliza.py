"""
Canine Classifier - Dog Breed Identification Tool
Identify your dog's breed using AI, questionnaire, or dichotomous key.
"""

import logging
import sqlite3
import os

log = logging.getLogger(__name__)

# Import UI utilities
try:
    from ui_utils import (
        Colors, SIMPLE_BANNER, print_colored, print_header, print_subheader,
        print_menu_option, print_success, print_error, print_warning, print_info,
        print_divider, print_box, loading_animation, get_input, get_choice,
        print_result_card, print_breed_result, confidence_bar, clear_screen
    )
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    class Colors:
        RESET = BOLD = BRIGHT_WHITE = BRIGHT_CYAN = BRIGHT_YELLOW = BRIGHT_GREEN = BRIGHT_RED = DIM = ""


class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dog_database.db')
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def fetch_dog_breeds(self, color, ear_type, tail_type, size, coat_type):
        query = """
        SELECT DogBreeds.BreedName,
               SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) AS MatchedAttributes,
               ROUND((SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) / 5.0) * 100, 2) AS Probability
        FROM DogBreeds
        LEFT JOIN BreedColors ON DogBreeds.BreedID = BreedColors.BreedID
        LEFT JOIN DogColors ON BreedColors.ColorID = DogColors.ColorID
        WHERE DogColors.ColorName = ? OR DogColors.ColorName IS NULL
        GROUP BY DogBreeds.BreedName
        ORDER BY MatchedAttributes DESC, DogBreeds.BreedName
        LIMIT 3;
        """
        try:
            self.cursor.execute(query, (color, coat_type, ear_type, tail_type, size, color, coat_type, ear_type, tail_type, size, color))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as err:
            print("Something went wrong: {}".format(err))
            return []

    def close(self):
        self.cursor.close()
        self.db.close()


class DogBreedQuestions:
    def __init__(self):
        self.database = Database()

    def ask_question(self, question, options, display_options):
        """Ask a styled question with options."""
        if UI_AVAILABLE:
            print(f"\n  {Colors.BRIGHT_CYAN}?{Colors.RESET} {Colors.BRIGHT_WHITE}{question}{Colors.RESET}")
            print(f"    {Colors.DIM}Options: {display_options}{Colors.RESET}")
            print()
        else:
            print(f"\n{question}")
            print(f"Options: {display_options}")

        while True:
            if UI_AVAILABLE:
                user_input = input(f"  {Colors.BRIGHT_CYAN}▶{Colors.RESET} {Colors.BRIGHT_WHITE}Your answer:{Colors.RESET} ").strip().lower()
            else:
                user_input = input("Your answer: ").strip().lower()

            if user_input in options:
                if UI_AVAILABLE:
                    print(f"    {Colors.BRIGHT_GREEN}✓ {user_input.capitalize()}{Colors.RESET}")
                return user_input
            else:
                if UI_AVAILABLE:
                    print(f"    {Colors.BRIGHT_RED}✗ Invalid option. Please try again.{Colors.RESET}")
                else:
                    print("Invalid option. Please try again.")

    def determine_dog_breeds(self):
        """Run the questionnaire to determine dog breeds."""
        valid_colors = ["black", "white", "brown", "tan", "brindle", "merle", "chocolate", "yellow"]
        valid_ear_types = ["floppy", "tall", "triangular"]
        valid_tail_types = ["docked", "long_and_curved", "curled"]
        valid_sizes = ["small", "medium", "large", "giant"]
        valid_coat_types = ["short", "medium", "long", "curly", "double", "smooth", "dense", "silky"]

        if UI_AVAILABLE:
            print_header("QUESTIONNAIRE MODE", Colors.BRIGHT_MAGENTA)
            print_info("Answer questions about your dog's physical characteristics.")
            print_divider()

        color = self.ask_question(
            "What is the COLOR of your dog?",
            valid_colors,
            "Black, White, Brown, Tan, Brindle, Merle, Chocolate, Yellow"
        )
        ear_type = self.ask_question(
            "What is the EAR TYPE of your dog?",
            valid_ear_types,
            "Floppy, Tall, Triangular"
        )
        tail_type = self.ask_question(
            "What is the TAIL TYPE of your dog?",
            valid_tail_types,
            "Docked, Long_and_curved, Curled"
        )
        size = self.ask_question(
            "What is the SIZE of your dog?",
            valid_sizes,
            "Small, Medium, Large, Giant"
        )
        coat_type = self.ask_question(
            "What is the COAT TYPE of your dog?",
            valid_coat_types,
            "Short, Medium, Long, Curly, Double, Smooth, Dense, Silky"
        )

        # Capitalize color to match database format
        color = color.capitalize()

        if UI_AVAILABLE:
            print()
            print_divider()
            loading_animation("Analyzing breed matches", 1.0)

        breed_results = self.database.fetch_dog_breeds(color, ear_type, tail_type, size, coat_type)

        if breed_results:
            if UI_AVAILABLE:
                print_header("BREED MATCHES", Colors.BRIGHT_GREEN)
                print()
                for i, (breed, matched_attributes, probability) in enumerate(breed_results, 1):
                    print_breed_result(i, breed, probability)
                    print(f"      {Colors.DIM}Matched {int(matched_attributes)}/5 attributes{Colors.RESET}")
                    print()
            else:
                print("\nBased on the provided attributes, the probabilities are:")
                for breed, matched_attributes, probability in breed_results:
                    print(f"{breed}: {probability}% probability (Matched: {matched_attributes}/5)")
        else:
            if UI_AVAILABLE:
                print_warning("No matching breeds found in database.")
                print_info("Try different attribute combinations.")
            else:
                print("Sorry, we couldn't determine any dog breeds.")

        self.database.close()


def run_image_classifier():
    """Run the AI image classification mode."""
    if UI_AVAILABLE:
        print_header("AI IMAGE RECOGNITION", Colors.BRIGHT_BLUE)
        print_info("Upload a photo to identify your dog's breed using AI.")
        print_divider()
        print()

    try:
        from image_classifier import DogImageClassifier
        classifier = DogImageClassifier()

        if UI_AVAILABLE:
            print(f"  {Colors.BRIGHT_CYAN}📷 Enter the path to your dog's photo{Colors.RESET}")
            print(f"     {Colors.DIM}(Drag and drop works too!){Colors.RESET}")
            print()
            image_path = input(f"  {Colors.BRIGHT_CYAN}▶{Colors.RESET} {Colors.BRIGHT_WHITE}Image path:{Colors.RESET} ").strip()
        else:
            image_path = input("Enter the path to your dog's photo: ").strip()

        # Remove quotes if user included them
        image_path = image_path.strip('"').strip("'")

        if image_path:
            if UI_AVAILABLE:
                print()
                loading_animation("Loading AI model", 0.5)

            results = classifier.classify_image(image_path)

            if results and UI_AVAILABLE:
                print_header("AI PREDICTION RESULTS", Colors.BRIGHT_GREEN)
                print()
                for i, (breed, confidence) in enumerate(results, 1):
                    print_breed_result(i, breed, confidence)
                print()
                print_divider()
                print_info("Results based on Google's Vision Transformer (ViT) model")
            elif results:
                classifier.display_results(results)
            else:
                if UI_AVAILABLE:
                    print_error("Could not classify the image.")
                else:
                    print("Could not classify the image.")
        else:
            if UI_AVAILABLE:
                print_warning("No image path provided.")
            else:
                print("No image path provided.")

    except ImportError as e:
        if UI_AVAILABLE:
            print_error("Could not load image classifier module.")
            print_info("Install required packages: pip install transformers torch torchvision Pillow")
        else:
            print(f"Error: Could not load image classifier. {e}")
    except Exception as e:
        if UI_AVAILABLE:
            print_error(f"Error during classification: {e}")
        else:
            print(f"Error: {e}")


def run_dichotomous_key():
    """Run the dichotomous key identification mode."""
    try:
        from dichotomous_key import DichotomousKey

        if UI_AVAILABLE:
            print_header("DICHOTOMOUS KEY", Colors.BRIGHT_YELLOW)
            print_info("Answer Yes/No questions to identify your dog's breed.")
            print_info("This method uses a biological classification approach.")
            print_divider()

        key = DichotomousKey()
        key.identify()

    except ImportError as e:
        if UI_AVAILABLE:
            print_error("Could not load dichotomous key module.")
        else:
            print(f"Error: {e}")
    except Exception as e:
        if UI_AVAILABLE:
            print_error(f"Error during identification: {e}")
        else:
            print(f"Error: {e}")


def show_main_menu():
    """Display the main menu."""
    if UI_AVAILABLE:
        clear_screen()
        print(SIMPLE_BANNER)
        print()
        print(f"  {Colors.BRIGHT_WHITE}Choose an identification method:{Colors.RESET}")
        print()
        print_menu_option("1", "Questionnaire", "📋", Colors.BRIGHT_MAGENTA)
        print(f"      {Colors.DIM}Answer questions about your dog's appearance{Colors.RESET}")
        print()
        print_menu_option("2", "AI Image Recognition", "🤖", Colors.BRIGHT_BLUE)
        print(f"      {Colors.DIM}Upload a photo for instant AI analysis{Colors.RESET}")
        print()
        print_menu_option("3", "Dichotomous Key", "🔬", Colors.BRIGHT_YELLOW)
        print(f"      {Colors.DIM}Yes/No branching questions (scientific method){Colors.RESET}")
        print()
        print_menu_option("4", "Exit", "👋", Colors.BRIGHT_RED)
        print()
        print_divider()
    else:
        print("=" * 55)
        print("   CANINE CLASSIFIER - Dog Breed Identification Tool")
        print("=" * 55)
        print("\nHow would you like to identify your dog?\n")
        print("  1. Answer questions about your dog's appearance")
        print("  2. Upload a photo of your dog (AI image recognition)")
        print("  3. Dichotomous key (Yes/No branching questions)")
        print("  4. Exit")
        print()


def main():
    """Main entry point."""
    show_main_menu()

    while True:
        if UI_AVAILABLE:
            choice = input(f"  {Colors.BRIGHT_CYAN}▶{Colors.RESET} {Colors.BRIGHT_WHITE}Enter your choice (1-4):{Colors.RESET} ").strip()
        else:
            choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            if UI_AVAILABLE:
                print_success("Starting Questionnaire Mode...")
            else:
                print("\nStarting questionnaire mode...\n")
            dog_questions = DogBreedQuestions()
            dog_questions.determine_dog_breeds()
            break

        elif choice == "2":
            if UI_AVAILABLE:
                print_success("Starting AI Image Recognition...")
            else:
                print("\nStarting image recognition mode...\n")
            run_image_classifier()
            break

        elif choice == "3":
            if UI_AVAILABLE:
                print_success("Starting Dichotomous Key...")
            run_dichotomous_key()
            break

        elif choice == "4":
            if UI_AVAILABLE:
                print()
                print(f"  {Colors.BRIGHT_YELLOW}🐕 Thanks for using Canine Classifier! Goodbye! 🐕{Colors.RESET}")
                print()
            else:
                print("\nGoodbye!")
            break

        else:
            if UI_AVAILABLE:
                print_error("Invalid choice. Please enter 1, 2, 3, or 4.")
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    main()
