"""
Breed Information Database
Comprehensive information about dog breeds including temperament, care needs, and characteristics.
"""

# Import UI utilities
try:
    from ui_utils import Colors, print_divider
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    class Colors:
        RESET = BOLD = BRIGHT_WHITE = BRIGHT_CYAN = BRIGHT_YELLOW = ""
        BRIGHT_GREEN = BRIGHT_RED = DIM = BRIGHT_BLUE = BRIGHT_MAGENTA = ""


# Comprehensive breed information database
BREED_INFO = {
    "golden retriever": {
        "name": "Golden Retriever",
        "group": "Sporting",
        "origin": "Scotland",
        "size": {"weight": "55-75 lbs", "height": "21-24 inches"},
        "lifespan": "10-12 years",
        "temperament": ["Friendly", "Intelligent", "Devoted", "Reliable"],
        "exercise": "High (1-2 hours daily)",
        "grooming": "Moderate (weekly brushing, more during shedding)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Excellent - eager to please",
        "barking": "Moderate",
        "shedding": "Heavy (seasonal)",
        "health_issues": ["Hip dysplasia", "Elbow dysplasia", "Cancer", "Heart issues"],
        "fun_fact": "Golden Retrievers are the 3rd most popular dog breed in America!",
        "similar_breeds": ["Labrador Retriever", "Flat-Coated Retriever", "Nova Scotia Duck Tolling Retriever"]
    },
    "labrador retriever": {
        "name": "Labrador Retriever",
        "group": "Sporting",
        "origin": "Canada (Newfoundland)",
        "size": {"weight": "55-80 lbs", "height": "21-24 inches"},
        "lifespan": "10-12 years",
        "temperament": ["Friendly", "Active", "Outgoing", "Gentle"],
        "exercise": "High (1-2 hours daily)",
        "grooming": "Low to Moderate (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Excellent - highly intelligent",
        "barking": "Moderate",
        "shedding": "Heavy (year-round)",
        "health_issues": ["Hip dysplasia", "Obesity", "Ear infections", "Eye conditions"],
        "fun_fact": "Labs have been the #1 most popular dog breed in America for 31 years!",
        "similar_breeds": ["Golden Retriever", "Chesapeake Bay Retriever", "Flat-Coated Retriever"]
    },
    "german shepherd": {
        "name": "German Shepherd",
        "group": "Herding",
        "origin": "Germany",
        "size": {"weight": "50-90 lbs", "height": "22-26 inches"},
        "lifespan": "9-13 years",
        "temperament": ["Confident", "Courageous", "Smart", "Loyal"],
        "exercise": "High (2+ hours daily)",
        "grooming": "Moderate (regular brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": False, "strangers": False},
        "trainability": "Excellent - highly trainable working dog",
        "barking": "High",
        "shedding": "Heavy (year-round, seasonal blowing)",
        "health_issues": ["Hip dysplasia", "Elbow dysplasia", "Bloat", "Degenerative myelopathy"],
        "fun_fact": "German Shepherds are used worldwide as police, military, and service dogs!",
        "similar_breeds": ["Belgian Malinois", "Dutch Shepherd", "King Shepherd"]
    },
    "poodle": {
        "name": "Poodle",
        "group": "Non-Sporting",
        "origin": "Germany/France",
        "size": {"weight": "40-70 lbs (Standard)", "height": "15+ inches (Standard)"},
        "lifespan": "12-15 years",
        "temperament": ["Intelligent", "Active", "Alert", "Proud"],
        "exercise": "Moderate to High (1 hour daily)",
        "grooming": "High (professional grooming every 4-6 weeks)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Excellent - 2nd smartest dog breed",
        "barking": "Moderate to High",
        "shedding": "Minimal (hypoallergenic)",
        "health_issues": ["Hip dysplasia", "Eye problems", "Bloat", "Addison's disease"],
        "fun_fact": "Poodles are the 2nd most intelligent dog breed after Border Collies!",
        "similar_breeds": ["Portuguese Water Dog", "Lagotto Romagnolo", "Irish Water Spaniel"]
    },
    "siberian husky": {
        "name": "Siberian Husky",
        "group": "Working",
        "origin": "Siberia, Russia",
        "size": {"weight": "35-60 lbs", "height": "20-23 inches"},
        "lifespan": "12-14 years",
        "temperament": ["Outgoing", "Mischievous", "Loyal", "Friendly"],
        "exercise": "Very High (2+ hours daily)",
        "grooming": "Moderate (weekly brushing, heavy during shedding)",
        "good_with": {"kids": True, "dogs": True, "cats": False, "strangers": True},
        "trainability": "Moderate - independent and stubborn",
        "barking": "High (howling)",
        "shedding": "Heavy (twice yearly blowing)",
        "health_issues": ["Hip dysplasia", "Eye problems", "Hypothyroidism"],
        "fun_fact": "Huskies can run up to 100 miles a day and withstand -60°F temperatures!",
        "similar_breeds": ["Alaskan Malamute", "Samoyed", "Akita"]
    },
    "boxer": {
        "name": "Boxer",
        "group": "Working",
        "origin": "Germany",
        "size": {"weight": "50-80 lbs", "height": "21-25 inches"},
        "lifespan": "10-12 years",
        "temperament": ["Playful", "Loyal", "Energetic", "Fearless"],
        "exercise": "High (1-2 hours daily)",
        "grooming": "Low (occasional brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": False},
        "trainability": "Good - can be stubborn but eager to please",
        "barking": "Moderate",
        "shedding": "Moderate",
        "health_issues": ["Cancer", "Heart conditions", "Hip dysplasia", "Bloat"],
        "fun_fact": "Boxers got their name from their tendency to play by standing on hind legs and 'boxing'!",
        "similar_breeds": ["American Bulldog", "Bullmastiff", "Cane Corso"]
    },
    "rottweiler": {
        "name": "Rottweiler",
        "group": "Working",
        "origin": "Germany",
        "size": {"weight": "80-135 lbs", "height": "22-27 inches"},
        "lifespan": "8-10 years",
        "temperament": ["Loyal", "Confident", "Protective", "Calm"],
        "exercise": "Moderate to High (1-2 hours daily)",
        "grooming": "Low (weekly brushing)",
        "good_with": {"kids": True, "dogs": False, "cats": False, "strangers": False},
        "trainability": "Good - needs experienced owner",
        "barking": "Low to Moderate",
        "shedding": "Moderate (seasonal)",
        "health_issues": ["Hip dysplasia", "Elbow dysplasia", "Heart problems", "Cancer"],
        "fun_fact": "Rottweilers were originally used to herd livestock and pull carts for butchers!",
        "similar_breeds": ["Doberman Pinscher", "German Shepherd", "Cane Corso"]
    },
    "doberman pinscher": {
        "name": "Doberman Pinscher",
        "group": "Working",
        "origin": "Germany",
        "size": {"weight": "60-100 lbs", "height": "24-28 inches"},
        "lifespan": "10-12 years",
        "temperament": ["Loyal", "Fearless", "Alert", "Intelligent"],
        "exercise": "High (2+ hours daily)",
        "grooming": "Low (minimal brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": False, "strangers": False},
        "trainability": "Excellent - highly intelligent",
        "barking": "Moderate to High",
        "shedding": "Low to Moderate",
        "health_issues": ["Dilated cardiomyopathy", "Hip dysplasia", "Von Willebrand's disease"],
        "fun_fact": "Dobermans are the 5th smartest dog breed and excel as guard dogs!",
        "similar_breeds": ["Rottweiler", "German Shepherd", "Weimaraner"]
    },
    "great dane": {
        "name": "Great Dane",
        "group": "Working",
        "origin": "Germany",
        "size": {"weight": "110-175 lbs", "height": "28-32 inches"},
        "lifespan": "7-10 years",
        "temperament": ["Friendly", "Patient", "Dependable", "Gentle"],
        "exercise": "Moderate (1 hour daily)",
        "grooming": "Low (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - eager to please but can be stubborn",
        "barking": "Low",
        "shedding": "Moderate",
        "health_issues": ["Bloat", "Hip dysplasia", "Heart disease", "Cancer"],
        "fun_fact": "Great Danes hold the record for tallest dog - Zeus was 44 inches tall!",
        "similar_breeds": ["Irish Wolfhound", "Scottish Deerhound", "Mastiff"]
    },
    "chihuahua": {
        "name": "Chihuahua",
        "group": "Toy",
        "origin": "Mexico",
        "size": {"weight": "3-6 lbs", "height": "5-8 inches"},
        "lifespan": "14-16 years",
        "temperament": ["Charming", "Sassy", "Loyal", "Alert"],
        "exercise": "Low (30 minutes daily)",
        "grooming": "Low (occasional brushing)",
        "good_with": {"kids": False, "dogs": True, "cats": True, "strangers": False},
        "trainability": "Moderate - can be stubborn",
        "barking": "High",
        "shedding": "Low to Moderate",
        "health_issues": ["Patellar luxation", "Heart problems", "Hydrocephalus", "Hypoglycemia"],
        "fun_fact": "Chihuahuas are the smallest dog breed but have the biggest brain-to-body ratio!",
        "similar_breeds": ["Papillon", "Toy Fox Terrier", "Italian Greyhound"]
    },
    "pomeranian": {
        "name": "Pomeranian",
        "group": "Toy",
        "origin": "Germany/Poland",
        "size": {"weight": "3-7 lbs", "height": "6-7 inches"},
        "lifespan": "12-16 years",
        "temperament": ["Lively", "Bold", "Curious", "Playful"],
        "exercise": "Low to Moderate (30-45 minutes daily)",
        "grooming": "High (daily brushing recommended)",
        "good_with": {"kids": False, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - intelligent but can be stubborn",
        "barking": "High",
        "shedding": "Moderate to Heavy",
        "health_issues": ["Patellar luxation", "Collapsed trachea", "Dental issues", "Alopecia"],
        "fun_fact": "Queen Victoria had a Pomeranian, which helped popularize the breed!",
        "similar_breeds": ["German Spitz", "Japanese Spitz", "American Eskimo Dog"]
    },
    "shih tzu": {
        "name": "Shih Tzu",
        "group": "Toy",
        "origin": "China/Tibet",
        "size": {"weight": "9-16 lbs", "height": "9-10.5 inches"},
        "lifespan": "10-18 years",
        "temperament": ["Affectionate", "Playful", "Outgoing", "Gentle"],
        "exercise": "Low (30 minutes daily)",
        "grooming": "High (daily brushing, regular professional grooming)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Moderate - can be stubborn",
        "barking": "Moderate",
        "shedding": "Low (hypoallergenic)",
        "health_issues": ["Eye problems", "Hip dysplasia", "Patellar luxation", "Breathing issues"],
        "fun_fact": "Shih Tzu means 'lion dog' in Chinese - they were bred for Chinese royalty!",
        "similar_breeds": ["Lhasa Apso", "Maltese", "Havanese"]
    },
    "yorkshire terrier": {
        "name": "Yorkshire Terrier",
        "group": "Toy",
        "origin": "England",
        "size": {"weight": "4-7 lbs", "height": "7-8 inches"},
        "lifespan": "11-15 years",
        "temperament": ["Feisty", "Affectionate", "Sprightly", "Tomboyish"],
        "exercise": "Low to Moderate (30 minutes daily)",
        "grooming": "High (daily brushing, regular trimming)",
        "good_with": {"kids": False, "dogs": True, "cats": True, "strangers": False},
        "trainability": "Moderate - stubborn but smart",
        "barking": "High",
        "shedding": "Minimal (hypoallergenic)",
        "health_issues": ["Patellar luxation", "Dental issues", "Collapsed trachea", "Hypoglycemia"],
        "fun_fact": "Yorkies were originally bred to catch rats in clothing mills!",
        "similar_breeds": ["Silky Terrier", "Maltese", "Toy Manchester Terrier"]
    },
    "pug": {
        "name": "Pug",
        "group": "Toy",
        "origin": "China",
        "size": {"weight": "14-18 lbs", "height": "10-13 inches"},
        "lifespan": "13-15 years",
        "temperament": ["Charming", "Mischievous", "Loving", "Sociable"],
        "exercise": "Low (30 minutes daily)",
        "grooming": "Low (weekly brushing, facial wrinkle cleaning)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Moderate - eager to please but easily distracted",
        "barking": "Low to Moderate",
        "shedding": "Heavy",
        "health_issues": ["Breathing problems", "Eye problems", "Hip dysplasia", "Obesity"],
        "fun_fact": "A group of pugs is called a 'grumble'!",
        "similar_breeds": ["French Bulldog", "Boston Terrier", "English Bulldog"]
    },
    "boston terrier": {
        "name": "Boston Terrier",
        "group": "Non-Sporting",
        "origin": "United States",
        "size": {"weight": "12-25 lbs", "height": "15-17 inches"},
        "lifespan": "11-13 years",
        "temperament": ["Friendly", "Bright", "Amusing", "Gentle"],
        "exercise": "Moderate (45 minutes - 1 hour daily)",
        "grooming": "Low (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - intelligent and eager to please",
        "barking": "Low",
        "shedding": "Low",
        "health_issues": ["Eye problems", "Breathing issues", "Patellar luxation", "Deafness"],
        "fun_fact": "Boston Terriers are nicknamed 'The American Gentleman' for their tuxedo-like markings!",
        "similar_breeds": ["French Bulldog", "Pug", "English Bulldog"]
    },
    "border collie": {
        "name": "Border Collie",
        "group": "Herding",
        "origin": "Scotland/England Border",
        "size": {"weight": "30-55 lbs", "height": "18-22 inches"},
        "lifespan": "12-15 years",
        "temperament": ["Intelligent", "Energetic", "Alert", "Responsive"],
        "exercise": "Very High (2+ hours daily)",
        "grooming": "Moderate (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": False, "strangers": False},
        "trainability": "Excellent - smartest dog breed!",
        "barking": "High",
        "shedding": "Heavy (seasonal)",
        "health_issues": ["Hip dysplasia", "Epilepsy", "Collie eye anomaly", "Deafness"],
        "fun_fact": "Border Collies are considered the most intelligent dog breed - they can learn over 1,000 words!",
        "similar_breeds": ["Australian Shepherd", "Shetland Sheepdog", "Belgian Tervuren"]
    },
    "australian shepherd": {
        "name": "Australian Shepherd",
        "group": "Herding",
        "origin": "United States (despite the name!)",
        "size": {"weight": "40-65 lbs", "height": "18-23 inches"},
        "lifespan": "12-15 years",
        "temperament": ["Smart", "Work-Oriented", "Exuberant", "Protective"],
        "exercise": "Very High (2+ hours daily)",
        "grooming": "Moderate to High (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": False},
        "trainability": "Excellent - highly intelligent",
        "barking": "Moderate to High",
        "shedding": "Heavy",
        "health_issues": ["Hip dysplasia", "Epilepsy", "Eye problems", "MDR1 gene mutation"],
        "fun_fact": "Despite their name, Aussies were actually developed in the United States!",
        "similar_breeds": ["Border Collie", "English Shepherd", "Miniature American Shepherd"]
    },
    "beagle": {
        "name": "Beagle",
        "group": "Hound",
        "origin": "England",
        "size": {"weight": "20-30 lbs", "height": "13-15 inches"},
        "lifespan": "10-15 years",
        "temperament": ["Merry", "Friendly", "Curious", "Determined"],
        "exercise": "Moderate to High (1 hour daily)",
        "grooming": "Low (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Moderate - easily distracted by scents",
        "barking": "High (howling/baying)",
        "shedding": "Moderate",
        "health_issues": ["Epilepsy", "Hip dysplasia", "Eye problems", "Hypothyroidism"],
        "fun_fact": "Beagles have about 220 million scent receptors (humans have just 5 million)!",
        "similar_breeds": ["Basset Hound", "Harrier", "Foxhound"]
    },
    "basset hound": {
        "name": "Basset Hound",
        "group": "Hound",
        "origin": "France",
        "size": {"weight": "40-65 lbs", "height": "Up to 15 inches"},
        "lifespan": "12-13 years",
        "temperament": ["Charming", "Patient", "Low-Key", "Stubborn"],
        "exercise": "Low to Moderate (30-60 minutes daily)",
        "grooming": "Low (weekly brushing, ear cleaning important)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Moderate - stubborn but food-motivated",
        "barking": "Moderate to High (howling)",
        "shedding": "Moderate",
        "health_issues": ["Ear infections", "Obesity", "Hip dysplasia", "Bloat"],
        "fun_fact": "Basset Hounds have the second-best sense of smell of any dog breed after Bloodhounds!",
        "similar_breeds": ["Beagle", "Bloodhound", "Dachshund"]
    },
    "dachshund": {
        "name": "Dachshund",
        "group": "Hound",
        "origin": "Germany",
        "size": {"weight": "16-32 lbs (Standard)", "height": "8-9 inches (Standard)"},
        "lifespan": "12-16 years",
        "temperament": ["Clever", "Stubborn", "Devoted", "Lively"],
        "exercise": "Moderate (30-60 minutes daily)",
        "grooming": "Low to Moderate (varies by coat type)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": False},
        "trainability": "Moderate - stubborn but smart",
        "barking": "High",
        "shedding": "Low to Moderate",
        "health_issues": ["Intervertebral disc disease", "Obesity", "Dental issues", "Eye problems"],
        "fun_fact": "Dachshund means 'badger dog' in German - they were bred to hunt badgers!",
        "similar_breeds": ["Basset Hound", "Pembroke Welsh Corgi", "Miniature Schnauzer"]
    },
    "cocker spaniel": {
        "name": "Cocker Spaniel",
        "group": "Sporting",
        "origin": "United States/England",
        "size": {"weight": "20-30 lbs", "height": "13-15 inches"},
        "lifespan": "10-14 years",
        "temperament": ["Happy", "Smart", "Gentle", "Playful"],
        "exercise": "Moderate (1 hour daily)",
        "grooming": "High (regular brushing and professional grooming)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - eager to please",
        "barking": "Moderate",
        "shedding": "Moderate",
        "health_issues": ["Ear infections", "Eye problems", "Hip dysplasia", "Allergies"],
        "fun_fact": "Lady from 'Lady and the Tramp' is a Cocker Spaniel!",
        "similar_breeds": ["English Springer Spaniel", "Cavalier King Charles Spaniel", "Field Spaniel"]
    },
    "cavalier king charles spaniel": {
        "name": "Cavalier King Charles Spaniel",
        "group": "Toy",
        "origin": "England",
        "size": {"weight": "12-18 lbs", "height": "12-13 inches"},
        "lifespan": "12-15 years",
        "temperament": ["Affectionate", "Gentle", "Graceful", "Playful"],
        "exercise": "Low to Moderate (30-60 minutes daily)",
        "grooming": "Moderate (regular brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - eager to please",
        "barking": "Low",
        "shedding": "Moderate",
        "health_issues": ["Heart disease (MVD)", "Syringomyelia", "Hip dysplasia", "Eye problems"],
        "fun_fact": "Named after King Charles II who was rarely seen without his spaniels!",
        "similar_breeds": ["Cocker Spaniel", "English Toy Spaniel", "Papillon"]
    },
    "shiba inu": {
        "name": "Shiba Inu",
        "group": "Non-Sporting",
        "origin": "Japan",
        "size": {"weight": "17-23 lbs", "height": "13-17 inches"},
        "lifespan": "13-16 years",
        "temperament": ["Alert", "Active", "Attentive", "Independent"],
        "exercise": "Moderate to High (1 hour daily)",
        "grooming": "Moderate (weekly brushing, heavy during shedding)",
        "good_with": {"kids": True, "dogs": False, "cats": False, "strangers": False},
        "trainability": "Moderate - independent and stubborn",
        "barking": "Low (but famous 'Shiba scream')",
        "shedding": "Heavy (twice yearly)",
        "health_issues": ["Allergies", "Hip dysplasia", "Patellar luxation", "Eye problems"],
        "fun_fact": "The 'Doge' meme features a Shiba Inu named Kabosu!",
        "similar_breeds": ["Akita", "Hokkaido", "Kai Ken"]
    },
    "chow chow": {
        "name": "Chow Chow",
        "group": "Non-Sporting",
        "origin": "China",
        "size": {"weight": "45-70 lbs", "height": "17-20 inches"},
        "lifespan": "8-12 years",
        "temperament": ["Dignified", "Aloof", "Serious", "Loyal"],
        "exercise": "Moderate (45 minutes - 1 hour daily)",
        "grooming": "High (daily brushing for rough coat)",
        "good_with": {"kids": False, "dogs": False, "cats": False, "strangers": False},
        "trainability": "Moderate - independent, needs experienced owner",
        "barking": "Low",
        "shedding": "Heavy (seasonal)",
        "health_issues": ["Hip dysplasia", "Eye problems", "Bloat", "Thyroid issues"],
        "fun_fact": "Chow Chows have blue-black tongues - one of only two breeds with this trait!",
        "similar_breeds": ["Shar-Pei", "Akita", "Samoyed"]
    },
    "bernese mountain dog": {
        "name": "Bernese Mountain Dog",
        "group": "Working",
        "origin": "Switzerland",
        "size": {"weight": "70-115 lbs", "height": "23-28 inches"},
        "lifespan": "7-10 years",
        "temperament": ["Good-Natured", "Calm", "Strong", "Affectionate"],
        "exercise": "Moderate (1 hour daily)",
        "grooming": "Moderate to High (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - eager to please",
        "barking": "Low to Moderate",
        "shedding": "Heavy",
        "health_issues": ["Cancer", "Hip dysplasia", "Elbow dysplasia", "Bloat"],
        "fun_fact": "Berners were originally used to pull carts in Swiss farms and can pull up to 1,000 lbs!",
        "similar_breeds": ["Greater Swiss Mountain Dog", "Saint Bernard", "Newfoundland"]
    },
    "saint bernard": {
        "name": "Saint Bernard",
        "group": "Working",
        "origin": "Switzerland/Italy",
        "size": {"weight": "120-180 lbs", "height": "26-30 inches"},
        "lifespan": "8-10 years",
        "temperament": ["Playful", "Charming", "Inquisitive", "Gentle"],
        "exercise": "Moderate (1 hour daily)",
        "grooming": "Moderate (weekly brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - willing to please",
        "barking": "Low",
        "shedding": "Heavy",
        "health_issues": ["Hip dysplasia", "Elbow dysplasia", "Bloat", "Heart problems"],
        "fun_fact": "Saint Bernards have saved over 2,000 lives in the Swiss Alps!",
        "similar_breeds": ["Bernese Mountain Dog", "Mastiff", "Newfoundland"]
    },
    "maltese": {
        "name": "Maltese",
        "group": "Toy",
        "origin": "Malta",
        "size": {"weight": "Under 7 lbs", "height": "7-9 inches"},
        "lifespan": "12-15 years",
        "temperament": ["Gentle", "Playful", "Charming", "Fearless"],
        "exercise": "Low (30 minutes daily)",
        "grooming": "High (daily brushing, regular professional grooming)",
        "good_with": {"kids": False, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - intelligent and responsive",
        "barking": "Moderate to High",
        "shedding": "Minimal (hypoallergenic)",
        "health_issues": ["Patellar luxation", "Heart problems", "Dental issues", "Eye problems"],
        "fun_fact": "Maltese have been companion dogs for over 2,000 years and were favorites of ancient royalty!",
        "similar_breeds": ["Bichon Frise", "Havanese", "Coton de Tulear"]
    },
    "shetland sheepdog": {
        "name": "Shetland Sheepdog",
        "group": "Herding",
        "origin": "Scotland (Shetland Islands)",
        "size": {"weight": "15-25 lbs", "height": "13-16 inches"},
        "lifespan": "12-14 years",
        "temperament": ["Playful", "Energetic", "Bright", "Affectionate"],
        "exercise": "Moderate to High (1 hour daily)",
        "grooming": "High (weekly brushing, more during shedding)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": False},
        "trainability": "Excellent - one of the smartest breeds",
        "barking": "High",
        "shedding": "Heavy",
        "health_issues": ["Eye problems", "Hip dysplasia", "Dermatomyositis", "Thyroid issues"],
        "fun_fact": "Shelties look like mini Collies and are one of the top 10 smartest dog breeds!",
        "similar_breeds": ["Collie", "Border Collie", "Australian Shepherd"]
    },
    "english setter": {
        "name": "English Setter",
        "group": "Sporting",
        "origin": "England",
        "size": {"weight": "45-80 lbs", "height": "23-27 inches"},
        "lifespan": "12 years",
        "temperament": ["Friendly", "Mellow", "Merry", "Gentle"],
        "exercise": "High (1-2 hours daily)",
        "grooming": "Moderate (regular brushing)",
        "good_with": {"kids": True, "dogs": True, "cats": True, "strangers": True},
        "trainability": "Good - eager to please but can be stubborn",
        "barking": "Moderate",
        "shedding": "Moderate",
        "health_issues": ["Hip dysplasia", "Elbow dysplasia", "Deafness", "Hypothyroidism"],
        "fun_fact": "English Setters are called 'setters' because they crouch or 'set' when they find game birds!",
        "similar_breeds": ["Irish Setter", "Gordon Setter", "Brittany"]
    }
}


def get_breed_info(breed_name):
    """Get breed information by name (case-insensitive, partial match)."""
    breed_lower = breed_name.lower().strip()

    # Direct match
    if breed_lower in BREED_INFO:
        return BREED_INFO[breed_lower]

    # Partial match
    for key, info in BREED_INFO.items():
        if breed_lower in key or key in breed_lower:
            return info

    return None


def display_breed_card(breed_name):
    """Display a beautiful breed information card."""
    info = get_breed_info(breed_name)

    if not info:
        if UI_AVAILABLE:
            print(f"\n  {Colors.BRIGHT_YELLOW}⚠ No detailed information available for {breed_name}{Colors.RESET}")
        else:
            print(f"\nNo detailed information available for {breed_name}")
        return

    if UI_AVAILABLE:
        # Header
        print(f"\n  {Colors.BRIGHT_CYAN}╔{'═' * 62}╗{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BOLD}{Colors.BRIGHT_WHITE}🐕 {info['name'].upper()}{Colors.RESET}{' ' * (57 - len(info['name']))}{Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╠{'═' * 62}╣{Colors.RESET}")

        # Basic info
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_YELLOW}Group:{Colors.RESET} {info['group']:15}  {Colors.BRIGHT_YELLOW}Origin:{Colors.RESET} {info['origin']:20}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_YELLOW}Size:{Colors.RESET} {info['size']['weight']:16}  {Colors.BRIGHT_YELLOW}Lifespan:{Colors.RESET} {info['lifespan']:17}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╠{'═' * 62}╣{Colors.RESET}")

        # Temperament
        temp_str = ", ".join(info['temperament'][:4])
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_GREEN}Temperament:{Colors.RESET} {temp_str:47}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")

        # Care needs
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_GREEN}Exercise:{Colors.RESET} {info['exercise']:50}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_GREEN}Grooming:{Colors.RESET} {info['grooming'][:50]:50}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_GREEN}Trainability:{Colors.RESET} {info['trainability'][:46]:46}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╠{'═' * 62}╣{Colors.RESET}")

        # Good with
        gw = info['good_with']
        kids = f"{Colors.BRIGHT_GREEN}✓{Colors.RESET}" if gw['kids'] else f"{Colors.BRIGHT_RED}✗{Colors.RESET}"
        dogs = f"{Colors.BRIGHT_GREEN}✓{Colors.RESET}" if gw['dogs'] else f"{Colors.BRIGHT_RED}✗{Colors.RESET}"
        cats = f"{Colors.BRIGHT_GREEN}✓{Colors.RESET}" if gw['cats'] else f"{Colors.BRIGHT_RED}✗{Colors.RESET}"
        strangers = f"{Colors.BRIGHT_GREEN}✓{Colors.RESET}" if gw['strangers'] else f"{Colors.BRIGHT_RED}✗{Colors.RESET}"
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_MAGENTA}Good with:{Colors.RESET}  Kids {kids}  Dogs {dogs}  Cats {cats}  Strangers {strangers}      {Colors.BRIGHT_CYAN}║{Colors.RESET}")

        # Additional info
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_MAGENTA}Barking:{Colors.RESET} {info['barking']:12}  {Colors.BRIGHT_MAGENTA}Shedding:{Colors.RESET} {info['shedding']:22}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╠{'═' * 62}╣{Colors.RESET}")

        # Health issues
        health = ", ".join(info['health_issues'][:3])
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_RED}Health Watch:{Colors.RESET} {health[:47]:47}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╠{'═' * 62}╣{Colors.RESET}")

        # Fun fact - wrap text properly
        fact = info['fun_fact']
        print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_YELLOW}💡 Fun Fact:{Colors.RESET}                                                {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        # Word wrap the fun fact
        words = fact.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= 56:
                current_line = (current_line + " " + word).strip()
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        for line in lines:
            print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}     {line:56}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╠{'═' * 62}╣{Colors.RESET}")

        # Similar breeds
        similar = ", ".join(info['similar_breeds'][:3])
        if len(similar) > 44:
            print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.DIM}Similar breeds:{Colors.RESET}                                            {Colors.BRIGHT_CYAN}║{Colors.RESET}")
            print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}     {Colors.DIM}{similar:56}{Colors.RESET}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        else:
            print(f"  {Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.DIM}Similar breeds: {similar:44}{Colors.RESET}  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}╚{'═' * 62}╝{Colors.RESET}")

    else:
        # Plain text output
        print(f"\n{'=' * 60}")
        print(f"  🐕 {info['name'].upper()}")
        print(f"{'=' * 60}")
        print(f"  Group: {info['group']}  |  Origin: {info['origin']}")
        print(f"  Size: {info['size']['weight']}  |  Lifespan: {info['lifespan']}")
        print(f"\n  Temperament: {', '.join(info['temperament'])}")
        print(f"  Exercise: {info['exercise']}")
        print(f"  Grooming: {info['grooming']}")
        print(f"  Trainability: {info['trainability']}")
        print(f"\n  Good with: Kids={'Yes' if info['good_with']['kids'] else 'No'}, Dogs={'Yes' if info['good_with']['dogs'] else 'No'}, Cats={'Yes' if info['good_with']['cats'] else 'No'}")
        print(f"  Barking: {info['barking']}  |  Shedding: {info['shedding']}")
        print(f"\n  Health Watch: {', '.join(info['health_issues'][:3])}")
        print(f"\n  💡 Fun Fact: {info['fun_fact']}")
        print(f"\n  Similar breeds: {', '.join(info['similar_breeds'])}")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    # Test display
    display_breed_card("Golden Retriever")
    display_breed_card("Poodle")
