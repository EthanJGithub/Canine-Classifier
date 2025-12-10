# Canine Classifier

**AI-Powered Dog Breed Identification System**

A professional-grade application that identifies dog breeds using multiple classification methods: AI image recognition, feature-based questionnaires, and scientific dichotomous keys. Built with a stunning 2025-level premium UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![AI](https://img.shields.io/badge/AI-Vision%20Transformer-purple.svg)

---

## Features

### 1. AI Image Recognition
Upload a photo of any dog and get instant breed predictions powered by Google's Vision Transformer (ViT) neural network.

- **Instant Results**: Analyze images in seconds
- **Top 5 Predictions**: Ranked by confidence percentage
- **Database Verification**: Cross-references AI predictions with local breed database
- **Supports**: JPG, PNG, WebP, GIF formats

### 2. Feature Questionnaire
Answer questions about your dog's physical characteristics to find matching breeds.

- **5 Key Attributes**: Color, Ear Type, Tail Type, Size, Coat Type
- **Probability Matching**: Calculates match percentage based on attributes
- **Top 3 Results**: Returns best-matching breeds from database

### 3. Scientific Dichotomous Key
Professional Yes/No identification method used by veterinarians and experts.

- **Binary Decision Tree**: Simple yes/no questions
- **Progressive Narrowing**: Each answer eliminates breeds
- **Scientific Approach**: Based on taxonomic classification methods

### 4. Comprehensive Breed Database
Explore detailed information on 51+ dog breeds worldwide.

- **Breed Profiles**: Origin, size, lifespan, temperament
- **Care Requirements**: Exercise needs, grooming, trainability
- **Compatibility Info**: Good with kids, dogs, cats, strangers
- **Health Information**: Common health issues and concerns
- **Fun Facts**: Interesting breed-specific trivia

---

## Screenshots

The application features a premium dark-themed UI with:
- Animated gradient effects
- Glass morphism cards
- Smooth hover transitions
- Responsive design that adapts to any screen size

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/canine-classifier.git
cd canine-classifier
```

### Step 2: Install Dependencies
```bash
pip install pillow transformers torch torchvision
```

### Step 3: Run the Application
```bash
python ElizaGUI.py
```

**Note**: On first run, the AI model (~350MB) will be downloaded automatically.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `tkinter` | GUI framework (included with Python) |
| `Pillow` | Image processing |
| `transformers` | Hugging Face AI models |
| `torch` | PyTorch deep learning |
| `torchvision` | Computer vision utilities |
| `sqlite3` | Local database (included with Python) |

---

## Project Structure

```
canine-classifier/
├── ElizaGUI.py          # Main application with premium UI
├── image_classifier.py  # AI image recognition engine
├── breed_info.py        # Comprehensive breed database (51 breeds)
├── dichotomous_key.py   # Scientific decision tree classifier
├── eliza.py             # Core classification logic
├── app.py               # REST API (Flask)
├── dog_database.db      # SQLite breed database
├── dog_database.sql     # Database schema
├── ui_utils.py          # Terminal UI utilities
├── setup_model.py       # AI model downloader
└── README.md            # This file
```

---

## Usage Guide

### AI Recognition
1. Click **"AI Recognition"** on the home screen
2. Click the preview area or **"Browse Files"** to select an image
3. Click **"Analyze Image"**
4. View ranked breed predictions with confidence scores
5. Click any result to see detailed breed information

### Questionnaire
1. Click **"Feature Questionnaire"** on the home screen
2. Select your dog's characteristics from the dropdowns:
   - Primary Color
   - Ear Type
   - Tail Type
   - Size
   - Coat Type
3. Click **"Find Matching Breeds"**
4. View matching breeds ranked by probability

### Dichotomous Key
1. Click **"Dichotomous Key"** on the home screen
2. Answer each Yes/No question about your dog
3. Continue until a breed is identified
4. View the result and detailed breed information

### Breed Database
1. Click **"Breed Database"** on the home screen
2. Browse all breeds in the grid view
3. Click any breed to see detailed information
4. Use the search box to find specific breeds

---

## API Usage

The application includes a REST API for programmatic access:

```python
import requests

response = requests.post('http://localhost:5000/determine_breed', json={
    'color': 'Black',
    'ear_type': 'floppy',
    'tail_type': 'long_and_curved',
    'size': 'large',
    'coat_type': 'short'
})

print(response.json())
```

Start the API server:
```bash
python app.py
```

---

## Breed Database Coverage

The database includes detailed profiles for 51 breeds across all major groups:

**Sporting**: Golden Retriever, Labrador Retriever, Cocker Spaniel, English Setter, Weimaraner, Vizsla, Irish Setter

**Working**: German Shepherd, Boxer, Rottweiler, Doberman, Great Dane, Saint Bernard, Bernese Mountain Dog, Siberian Husky, Alaskan Malamute, Akita, Mastiff, Newfoundland, Samoyed, Great Pyrenees, Cane Corso

**Herding**: Border Collie, Australian Shepherd, Shetland Sheepdog, Collie, Pembroke Welsh Corgi

**Hound**: Beagle, Basset Hound, Dachshund, Bloodhound, Whippet, Rhodesian Ridgeback

**Toy**: Chihuahua, Pomeranian, Shih Tzu, Yorkshire Terrier, Pug, Maltese, Cavalier King Charles Spaniel, Havanese, Bichon Frise

**Terrier**: Miniature Schnauzer, Jack Russell Terrier, West Highland White Terrier

**Non-Sporting**: Poodle, Boston Terrier, French Bulldog, English Bulldog, Shiba Inu, Chow Chow

---

## Technical Details

### AI Model
- **Model**: Google Vision Transformer (ViT-base-patch16-224)
- **Source**: Hugging Face Transformers
- **Training**: Pre-trained on ImageNet (1000+ categories)
- **Accuracy**: ~90% on standard dog breed datasets

### Database
- **Engine**: SQLite (portable, no server required)
- **Schema**: Normalized with breed attributes and color mappings
- **Size**: ~24KB (lightweight and fast)

### UI Framework
- **Toolkit**: Tkinter with custom canvas widgets
- **Design**: Glass morphism with animated effects
- **Responsive**: Adapts to screen size automatically
- **DPI Aware**: Crisp rendering on high-DPI displays

---

## Roadmap

- [ ] Expand breed database to 200+ breeds
- [ ] Add mixed breed detection
- [ ] Health risk scoring engine
- [ ] Mobile app (iOS/Android)
- [ ] Cloud API with authentication
- [ ] Breed comparison tool
- [ ] Training and nutrition recommendations

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Google Vision Transformer team for the AI model
- Hugging Face for the Transformers library
- The dog breeding community for breed information
- All contributors and testers

---

## Contact

For questions, suggestions, or business inquiries:

- **Issues**: [GitHub Issues](https://github.com/yourusername/canine-classifier/issues)
- **Email**: your.email@example.com

---

**Made with love for dogs everywhere**
