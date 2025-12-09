import logging
import sqlite3
import os

log = logging.getLogger(__name__)

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

    def ask_question(self, question, options):
        print(f"\n{question}")
        while True:
            user_input = input("").strip().lower()
            if user_input in options:
                return user_input
            else:
                print("\nIt seems there was an issue with your response. Please try again.")


    def determine_dog_breeds(self):
        valid_colors = ["black", "white", "brown", "tan", "brindle", "merle", "chocolate", "yellow"]
        valid_ear_types = ["floppy", "tall", "triangular"]
        valid_tail_types = ["docked", "long_and_curved", "curled"]
        valid_sizes = ["small", "medium", "large", "giant"]
        valid_coat_types = ["short", "medium", "long", "curly", "double", "smooth", "dense", "silky"]

        color = self.ask_question("What is the color of your dog? (Black, White, Brown, Tan, Brindle, Merle, Chocolate, Yellow)", valid_colors)
        ear_type = self.ask_question("What is the ear type of your dog? (Floppy, Tall, Triangular)", valid_ear_types)
        tail_type = self.ask_question("What is the tail type of your dog? (Docked, Long_and_curved, Curled)", valid_tail_types)
        size = self.ask_question("What is the size of your dog? (Small, Medium, Large, Giant)", valid_sizes)
        coat_type = self.ask_question("What is the coat type of your dog? (Short, Medium, Long, Curly, Double, Smooth, Dense, Silky)", valid_coat_types)

        # Capitalize color to match database format
        color = color.capitalize()
        print("Input values:", color, ear_type, tail_type, size, coat_type)

        breed_results = self.database.fetch_dog_breeds(color, ear_type, tail_type, size, coat_type)

        if breed_results:
            print("Based on the provided attributes, the probabilities of matching various breeds are:")
            for breed, matched_attributes, probability in breed_results:
                print(f"{breed}: {probability}% probability (Matched attributes: {matched_attributes}/5)")
        else:
            print("Sorry, we couldn't determine any dog breeds based on the provided attributes.")

        self.database.close()

def main():
    print("=" * 55)
    print("   CANINE CLASSIFIER - Dog Breed Identification Tool")
    print("=" * 55)
    print("\nHow would you like to identify your dog?\n")
    print("  1. Answer questions about your dog's appearance")
    print("  2. Upload a photo of your dog (AI image recognition)")
    print("  3. Dichotomous key (Yes/No branching questions)")
    print("  4. Exit")
    print()

    while True:
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            print("\nStarting questionnaire mode...\n")
            dog_questions = DogBreedQuestions()
            dog_questions.determine_dog_breeds()
            break

        elif choice == "2":
            print("\nStarting image recognition mode...\n")
            try:
                from image_classifier import DogImageClassifier
                classifier = DogImageClassifier()

                image_path = input("Enter the path to your dog's photo: ").strip()
                # Remove quotes if user included them
                image_path = image_path.strip('"').strip("'")

                if image_path:
                    results = classifier.classify_image(image_path)
                    classifier.display_results(results)
                else:
                    print("No image path provided.")
            except ImportError as e:
                print(f"\nError: Could not load image classifier module.")
                print("Make sure image_classifier.py is in the same directory.")
                print(f"Details: {e}")
            except Exception as e:
                print(f"\nError during image classification: {e}")
            break

        elif choice == "3":
            try:
                from dichotomous_key import DichotomousKey
                key = DichotomousKey()
                key.identify()
            except ImportError as e:
                print(f"\nError: Could not load dichotomous key module.")
                print(f"Details: {e}")
            except Exception as e:
                print(f"\nError during identification: {e}")
            break

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    main()

