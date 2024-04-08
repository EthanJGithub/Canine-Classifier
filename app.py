from flask import Flask, request, jsonify
from eliza import DogBreedQuestions  # Import your DogBreedQuestions class

app = Flask(__name__)

@app.route('/determine_breed', methods=['POST'])
def determine_breed():
    # Parse the incoming JSON data
    data = request.json

    # Extract attributes from the data
    color = data.get('color')
    ear_type = data.get('ear_type')
    tail_type = data.get('tail_type')
    size = data.get('size')
    coat_type = data.get('coat_type')

    # Initialize your DogBreedQuestions class (or equivalent logic)
    dog_questions = DogBreedQuestions()

    # Assuming determine_dog_breeds returns a list of strings as results
    # Modify this part according to how your DogBreedQuestions class is implemented
    results = dog_questions.determine_dog_breeds(color, ear_type, tail_type, size, coat_type, interactive=False)

    # Return the results as a JSON response
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
