#Importoidaan kirjasto random satunnaisten lukujen valitsemiseen 
import random
#Importoidaan kirjasto re säännöllisten ilmausten käyttämiiseen, kun pelaaja syöttää koordinaatit. Näillä tarkastetaan koordinaattien oikea muoto.
import re

# Luomme alueen laivoille
board = [['|_|'] * 10 for _ in range(10)]

# Laivojen kokojen luettelo
ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# Sanakirja kirjainten koordinaattien muuttamiseksi numerokoordinaateiksi
letter_to_number = {chr(65 + i): i for i in range(10)}

# Kokonaislaukausten laskeminen
total_shots = 0

# Käytetyt laukauskoordinaatit
used_shots = set()

# 1. Laivan sijoittaminen
def place_ships():
    for size in ship_sizes:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            orientation = random.choice(['horizontal', 'vertical'])
            if can_place_ship(x, y, size, orientation):
                place_ship(x, y, size, orientation)
                break

#  2. Laivan sijoituksen mahdollisuuden tarkistus annetuilla koordinaateilla
def can_place_ship(x, y, size, orientation):
    if orientation == 'horizontal':
        if y + size > 10:
            return False
        for i in range(size):
            if not is_valid_cell(x, y + i):
                return False  
    elif orientation == 'vertical':
        if x + size > 10:
            return False
        for i in range(size):
            if not is_valid_cell(x + i, y):
                return False
    return True

# 3. Onko annettu koordinaatti (x, y) kelvollinen pelilaudan ruutu
def is_valid_cell(x, y):
    if (
        board[x][y] == '|_|' and
        all(board[i][j] == '|_|' for i in range(max(0, x - 1), min(10, x + 2)) for j in range(max(0, y - 1), min(10, y + 2)))
    ):
        return True
    return False

# 4. Laivan sijoittaminen annetuille koordinaateille
def place_ship(x, y, size, orientation):
    for i in range(size):
        if orientation == 'horizontal':
            board[x][y + i] = '|X|'
        elif orientation == 'vertical':
            board[x + i][y] = '|X|'

# Kentän tulostaminen näytölle
def print_board(hidden):
    print('   1   2   3   4   5   6   7   8   9   10')
    for i, row in enumerate(board):
        if hidden:
            row = ['|_|' if cell == '|X|' else cell for cell in row]
        print(chr(65 + i), ' '.join(row))

# Koordinaattien muuntaminen "A7" -muodosta numeerisiin arvoihin
def parse_coordinates(coord):
    # Tarkista säännölistä ilmaisua käyttäen, onko annettujen koordinaattien ensimmäinen merkki iso tai pieni kirjain välillä a-j, toinen merkki numero välillä 1-9 ja mahdollinen kolmas merkki numero välillä 0-9.
    # Jos ei, tulosta teksti ja palauta tyhjät arvot.
    if not re.match(r'^[A-Ja-j][1-9][0]?$', coord):
        print("Virheellinen syöte! Käytä koordinaattimuotoa A-J ja 1-10")
        return None, None
    # Muuta koordinattien ensimmäinen merkki isoksi kirjaimeksi käyttäen letter_to_number- sanakirjaa. 
    x = letter_to_number[coord[0].upper()]
    # Muuta koordinaattien numero indeksissa 1 kokonaisluvuksi ja vähennä yksi (koska pelilaudalla ensimmäinen numero on 1)
    y = int(coord[1:]) - 1
    # Palauta koordinaatit tuplena
    return x, y

# 5. Osuvuuden tarkistus
def check_shot(x, y):
    global total_shots
    global used_shots

    if (x, y) in used_shots:
        print("Laukaus on jo annettu kyseisiin koordinaatteihin!")
        return None

    used_shots.add((x, y))
    total_shots += 1

    if board[x][y] == '|X|':
        board[x][y] = '|Х|'
        if all(cell == '|Х|' for row in board for cell in row if cell == '|X|'):
            return 'win'
        return 'hit'
    elif board[x][y] == '|_|':
        board[x][y] = '|.|'
        return 'miss'

# 6. Peli alkaa
def play_game():
    place_ships()
    print("Tervetuloa peliin 'Laivanupotus'!")
    player_name = input("Syötä nimesi: ")
    print("Laukaukset merkitään symboleilla '|X|' ja '|.|'.")
    print("Peli alkaa,", player_name + "!")

    global total_shots
    total_shots = 0

    while True:
        print_board(hidden=True)
        target = input("Syötä laukauksen koordinaatit: ")
        x, y = parse_coordinates(target)
        if x is None or y is None:
            continue
        result = check_shot(x, y)
        if result == 'hit':
            print("Osuma!")
        elif result == 'miss':
            print("Ohi!")
        elif result == 'win':
            board[x][y] = '|Х|'
            print_board(hidden=False)
            print("Onneksi olkoon. Voitit pelin!")
            print("Kokonaislaukaukset:", total_shots)
            break

# 7. Kysyy käyttäjältä, haluaako hän pelata uudelleen 
    while True:
        play_again = input("Haluatko pelata vielä kerran? (y/n): ")
        if play_again.lower() == 'y':
            reset_board()
            play_game()
            break
        elif play_again.lower() == 'n':
            show_scores()
            break
        else:
            print("Vastauksesi ei vastaa ehdotettua vastausta.")

# Palauttaa pelilaudan alkutilaan. Käytetään tilanteessa, jossa peli on päättynyt ja pelaaja haluaa aloittaa uuden pelin.
def reset_board():
    for i in range(10):
        for j in range(10):
            board[i][j] = '|_|'

# Tallennetaan pelin tulos tiedostoon
def save_score(player_name, shots):
    score = f"{player_name} - {shots} laukauksia"
    with open('score.txt', 'a') as file:
        file.write(score + "\n")

# 8. Näyttää muiden pelaajien tulokset
def show_scores():
    while True:
        show = input("Haluatko nähdä muiden pelaajien tulokset? (y/n): ")
        if show.lower() == 'y':
            try:
                with open('score.txt', 'r') as file:
                    scores = file.readlines()
                    scores.sort(key=lambda x: int(x.split(' - ')[-1].split()[0]))
                    print("Pelaajien tulokset:")
                    for score in scores:
                        print(score.strip())
                    break
            except FileNotFoundError:
                print("Tulostiedostoa ei löytynyt.")
                break
        elif show.lower() == 'n':
            print("Kiitos pelistä!")
            break
        else:
            print("Vastauksesi ei vastaa ehdotettua vastausta.")

# Peli käynnistyy
play_game()
