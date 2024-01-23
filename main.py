import random

def generate_random_note():
    # Notes in Western music
    notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    # Adding some dissonance with sharps and flats
    accidentals = ['', '#', 'b']
    return random.choice(notes) + random.choice(accidentals)

def generate_uncomfortable_rhythm():
    # Unusual rhythms: Using fractions like 1/8, 1/16, etc.
    rhythms = ['1/4', '1/8', '1/16', '3/8']
    return random.choice(rhythms)

def create_concerto(length):
    concerto = []
    for _ in range(length):
        note = generate_random_note()
        rhythm = generate_uncomfortable_rhythm()
        concerto.append(f"{note} ({rhythm})")
    return concerto

def create_multiple_concertos(number_of_concertos, length_of_each):
    all_concertos = []
    for _ in range(number_of_concertos):
        concerto = create_concerto(length_of_each)
        all_concertos.append(concerto)
    return all_concertos

# Example: Generate 3 random and uncomfortable concertos, each with 5 elements
multiple_concertos = create_multiple_concertos(3, 5)
print(multiple_concertos)
