import unittest
from unittest.mock import patch
from io import StringIO
from eliza import DogBreedQuestions    

# Five automated unit tests for different dog breeds (Poodle, Labrador Retriever, Shiba Inu, Chihuahua, and English Setter) verifying that the program is working as intended
class ElizaTest(unittest.TestCase):
   
    # Test method for determining dog breeds with Poodle as the expected result
    @patch('eliza.DogBreedQuestions.ask_question', side_effect=['black', 'floppy', 'curled', 'medium', 'long'])  
    @patch('eliza.Database.fetch_dog_breeds')  
    def test_determine_dog_breeds_poodle(self, mock_fetch_dog_breeds, mock_ask_question):  
       
        # Define the expected output based on the provided input and mock response
        expected_output = "Input values: black floppy curled medium long\nBased on the provided attributes, the probabilities of matching various breeds are:\nPoodle: 100.0% probability (Matched attributes: 5/5)\nSiberian Husky: 60.0% probability (Matched attributes: 3/5)\nBorder Collie: 40.0% probability (Matched attributes: 2/5)\n"
       
        # Mock the return value of fetch_dog_breeds method
        mock_fetch_dog_breeds.return_value = [
            ('Poodle', 5, 100.0),  
            ('Siberian Husky', 3, 60.0),
            ('Border Collie', 2, 40.0)
        ]
       
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Instantiate the DogBreedQuestions class
            dog_questions = DogBreedQuestions()  
            # Call the method to determine dog breeds
            dog_questions.determine_dog_breeds()  
            # Assert that the printed output matches the expected output
            self.assertEqual(fake_out.getvalue(), expected_output)

    # Test method for determining dog breeds with Labrador Retriever as the expected result
    @patch('eliza.DogBreedQuestions.ask_question', side_effect=['black', 'floppy', 'curled', 'large', 'short'])  
    @patch('eliza.Database.fetch_dog_breeds')  
    def test_determine_dog_breeds_labrador(self, mock_fetch_dog_breeds, mock_ask_question):  
       
        # Define the expected output based on the provided input and mock response
        expected_output = "Input values: black floppy curled large short\nBased on the provided attributes, the probabilities of matching various breeds are:\nLabrador Retriever: 100.0% probability (Matched attributes: 5/5)\nBoxer: 40.0% probability (Matched attributes: 2/5)\n"
       
        # Mock the return value of fetch_dog_breeds method
        mock_fetch_dog_breeds.return_value = [
            ('Labrador Retriever', 5, 100.0),  
            ('Boxer', 2, 40.0)
        ]
       
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Instantiate the DogBreedQuestions class
            dog_questions = DogBreedQuestions()  
            # Call the method to determine dog breeds
            dog_questions.determine_dog_breeds()  
            # Assert that the printed output matches the expected output
            self.assertEqual(fake_out.getvalue(), expected_output)
    
    # Test method for determining dog breeds with Shiba Inu as the expected result
    @patch('eliza.DogBreedQuestions.ask_question', side_effect=['black', 'triangular', 'curled', 'medium', 'double'])  
    @patch('eliza.Database.fetch_dog_breeds')  
    def test_determine_dog_breeds_shiba_inu(self, mock_fetch_dog_breeds, mock_ask_question):  
       
        # Define the expected output based on the provided input and mock response
        expected_output = "Input values: black triangular curled medium double\nBased on the provided attributes, the probabilities of matching various breeds are:\nShiba Inu: 100.0% probability (Matched attributes: 5/5)\nSiberian Husky: 60.0% probability (Matched attributes: 3/5)\nBorder Collie: 40.0% probability (Matched attributes: 2/5)\n"
       
        # Mock the return value of fetch_dog_breeds method
        mock_fetch_dog_breeds.return_value = [
            ('Shiba Inu', 5, 100.0),  
            ('Siberian Husky', 3, 60.0),
            ('Border Collie', 2, 40.0)
        ]
       
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Instantiate the DogBreedQuestions class
            dog_questions = DogBreedQuestions()  
            # Call the method to determine dog breeds
            dog_questions.determine_dog_breeds()  
            # Assert that the printed output matches the expected output
            self.assertEqual(fake_out.getvalue(), expected_output)

    # Test method for determining dog breeds with Chihuahua as the expected result
    @patch('eliza.DogBreedQuestions.ask_question', side_effect=['brown', 'triangular', 'curled', 'small', 'short'])  
    @patch('eliza.Database.fetch_dog_breeds')  
    def test_determine_dog_breeds_chihuahua(self, mock_fetch_dog_breeds, mock_ask_question):  
       
        # Define the expected output based on the provided input and mock response
        expected_output = "Input values: brown triangular curled small short\nBased on the provided attributes, the probabilities of matching various breeds are:\nChihuahua: 100.0% probability (Matched attributes: 5/5)\nSiberian Husky: 60.0% probability (Matched attributes: 3/5)\nBorder Collie: 40.0% probability (Matched attributes: 2/5)\n"
       
        # Mock the return value of fetch_dog_breeds method
        mock_fetch_dog_breeds.return_value = [
            ('Chihuahua', 5, 100.0),  
            ('Siberian Husky', 3, 60.0),
            ('Border Collie', 2, 40.0)
        ]
       
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Instantiate the DogBreedQuestions class
            dog_questions = DogBreedQuestions()  
            # Call the method to determine dog breeds
            dog_questions.determine_dog_breeds()  
            # Assert that the printed output matches the expected output
            self.assertEqual(fake_out.getvalue(), expected_output)

    # Test method for determining dog breeds with English Setter as the expected result
    @patch('eliza.DogBreedQuestions.ask_question', side_effect=['black', 'triangular', 'long_and_curved', 'large', 'medium'])  
    @patch('eliza.Database.fetch_dog_breeds')  
    def test_determine_dog_breeds_english_setter(self, mock_fetch_dog_breeds, mock_ask_question):  
       
        # Define the expected output based on the provided input and mock response
        expected_output = "Input values: black triangular long_and_curved large medium\nBased on the provided attributes, the probabilities of matching various breeds are:\nEnglish Setter: 100.0% probability (Matched attributes: 5/5)\nSiberian Husky: 60.0% probability (Matched attributes: 3/5)\nBorder Collie: 40.0% probability (Matched attributes: 2/5)\n"
       
        # Mock the return value of fetch_dog_breeds method
        mock_fetch_dog_breeds.return_value = [
            ('English Setter', 5, 100.0),  
            ('Siberian Husky', 3, 60.0),
            ('Border Collie', 2, 40.0)
        ]
       
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Instantiate the DogBreedQuestions class
            dog_questions = DogBreedQuestions()  
            # Call the method to determine dog breeds
            dog_questions.determine_dog_breeds()  
            # Assert that the printed output matches the expected output
            self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == '__main__':
    # Run the tests if the script is executed directly
    unittest.main()



