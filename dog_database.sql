-- Creation of DogBreeds table
CREATE TABLE DogBreeds (
    BreedID INT AUTO_INCREMENT PRIMARY KEY,
    BreedName VARCHAR(50) NOT NULL,
    Size ENUM('small', 'medium', 'large', 'giant'),
    CoatType ENUM('short', 'medium', 'long', 'curly', 'double', 'smooth', 'dense', 'weather_resistant', 'silky', 'hypoallergenic'),
    EarType ENUM('floppy', 'tall', 'triangular'),
    TailType ENUM('docked', 'long_and_curved', 'curled')
);

-- Creation of DogColors table
CREATE TABLE DogColors (
    ColorID INT AUTO_INCREMENT PRIMARY KEY,
    ColorName VARCHAR(50) NOT NULL
);

-- Creation of BreedColors linking table
CREATE TABLE BreedColors (
    BreedID INT,
    ColorID INT,
    FOREIGN KEY (BreedID) REFERENCES DogBreeds(BreedID),
    FOREIGN KEY (ColorID) REFERENCES DogColors(ColorID),
    PRIMARY KEY (BreedID, ColorID)
);

-- Insertion of dog breeds
INSERT INTO DogBreeds (BreedName, Size, CoatType, EarType, TailType) VALUES 
('Poodle', 'medium', 'curly', 'floppy', 'curled'),
('Boxer', 'large', 'short', 'tall', 'long_and_curved'),
('Siberian Husky', 'large', 'double', 'triangular', 'curled'),
('Dachshund', 'small', 'short', 'floppy', 'long_and_curved'),
('Rottweiler', 'large', 'dense', 'floppy', 'docked'),
('Shih Tzu', 'small', 'long', 'floppy', 'curled'),
('Great Dane', 'giant', 'short', 'tall', 'long_and_curved'),
('Doberman Pinscher', 'large', 'smooth', 'tall', 'docked'),
('Australian Shepherd', 'medium', 'medium', 'floppy', 'curled'),
('Chihuahua', 'small', 'short', 'triangular', 'curled'),
('Pomeranian', 'small', 'long', 'triangular', 'curled'),
('Yorkshire Terrier', 'small', 'silky', 'triangular', 'docked'),
('Pug', 'small', 'smooth', 'triangular', 'curled'),
('Shetland Sheepdog', 'small', 'long', 'floppy', 'long_and_curved'),
('Boston Terrier', 'small', 'short', 'triangular', 'curled'),
('Border Collie', 'medium', 'medium', 'floppy', 'long_and_curved'),
('Cocker Spaniel', 'medium', 'silky', 'floppy', 'curled'),
('Saint Bernard', 'giant', 'dense', 'floppy', 'long_and_curved'),
('Shiba Inu', 'medium', 'double', 'triangular', 'curled'),
('Chow Chow', 'medium', 'dense', 'triangular', 'curled'),
('Bernese Mountain Dog', 'large', 'long', 'floppy', 'curled'),
('Maltese', 'small', 'silky', 'triangular', 'curled'),
('Cavalier King Charles Spaniel', 'small', 'silky', 'floppy', 'curled'),
('Basset Hound', 'medium', 'short', 'floppy', 'curled'),
('English Setter', 'large', 'medium', 'floppy', 'long_and_curved');

-- Insertion of dog colors
INSERT INTO DogColors (ColorName) VALUES 
('Black'), 
('White'), 
('Brown'), 
('Tan'), 
('Brindle'), 
('Merle'), 
('Chocolate'), 
('Yellow');

-- Insertion of breed-color combinations

-- Poodle
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(1, 1), -- Black
(1, 2), -- White
(1, 3), -- Brown
(1, 4); -- Tan

-- Boxer
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(2, 1), -- Black
(2, 2), -- White
(2, 3), -- Brown
(2, 7); -- Chocolate

-- Siberian Husky
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(3, 1), -- Black
(3, 2), -- White
(3, 5), -- Brindle
(3, 4); -- Tan

-- Dachshund
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(4, 1), -- Black
(4, 2), -- White
(4, 3), -- Brown
(4, 4); -- Tan

-- Rottweiler
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(5, 1), -- Black
(5, 2), -- White
(5, 3), -- Brown
(5, 4); -- Tan

-- Shih Tzu
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(6, 1), -- Black
(6, 2), -- White
(6, 3), -- Brown
(6, 4); -- Tan

-- Great Dane
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(7, 1), -- Black
(7, 2), -- White
(7, 3), -- Brown
(7, 4); -- Tan

-- Doberman Pinscher
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(8, 1), -- Black
(8, 2), -- White
(8, 3), -- Brown
(8, 4); -- Tan

-- Australian Shepherd
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(9, 1), -- Black
(9, 2), -- White
(9, 5), -- Brindle
(9, 4); -- Tan

-- Chihuahua
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(10, 1), -- Black
(10, 2), -- White
(10, 3), -- Brown
(10, 4); -- Tan

-- Pomeranian
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(11, 1), -- Black
(11, 2), -- White
(11, 3), -- Brown
(11, 4); -- Tan

-- Yorkshire Terrier
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(12, 1), -- Black
(12, 2), -- White
(12, 3), -- Brown
(12, 4); -- Tan

-- Pug
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(13, 1), -- Black
(13, 2), -- White
(13, 3), -- Brown
(13, 4); -- Tan

-- Shetland Sheepdog
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(14, 1), -- Black
(14, 2), -- White
(14, 3), -- Brown
(14, 4); -- Tan

-- Boston Terrier
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(15, 1), -- Black
(15, 2), -- White
(15, 3), -- Brown
(15, 4); -- Tan

-- Border Collie
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(16, 1), -- Black
(16, 2), -- White
(16, 3), -- Brown
(16, 4); -- Tan

-- Cocker Spaniel
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(17, 1), -- Black
(17, 2), -- White
(17, 3), -- Brown
(17, 4); -- Tan

-- Saint Bernard
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(18, 1), -- Black
(18, 2), -- White
(18, 3), -- Brown
(18, 4); -- Tan

-- Shiba Inu
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(19, 1), -- Black
(19, 2), -- White
(19, 5), -- Brindle
(19, 4); -- Tan

-- Chow Chow
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(20, 1), -- Black
(20, 2), -- White
(20, 3), -- Brown
(20, 4); -- Tan

-- Bernese Mountain Dog
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(21, 1), -- Black
(21, 2), -- White
(21, 3), -- Brown
(21, 4); -- Tan

-- Maltese
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(22, 2), -- White
(22, 7); -- Chocolate

-- Cavalier King Charles Spaniel
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(23, 1), -- Black
(23, 2), -- White
(23, 3), -- Brown
(23, 4); -- Tan

-- Basset Hound
INSERT INTO BreedColors (BreedID, ColorID) VALUES 
(24, 1), -- Black
(24, 2), -- White
(24, 3), -- Brown
(24, 4); -- Tan

-- English Setter
INSERT INTO BreedColors (BreedID, ColorID) VALUES
(25, 1), -- Black
(25, 2); -- White
