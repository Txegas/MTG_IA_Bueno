from Card import Card
from Player import Player
from Game import Game

def create_test_deck():
    """Crea un mazo de prueba con cartas básicas."""
    return [
        Card(name="Llanowar Elves", mana_cost={}, card_types=["Creature"], subtypes=["Elf", "Druid"], text="{T}: Add {G}.", power=1, toughness=1, keyword_actions=["Tap"]),
        Card(name="Lightning Bolt", mana_cost={}, card_types=["Instant"], subtypes=[], text="Deal 3 damage to any target.")
    ] * 30  # Copia de cartas para un mazo de 60

# Crear jugadores
player1 = Player(name="Jugador 1", deck=create_test_deck())
player2 = Player(name="Jugador 2", deck=create_test_deck())

# Iniciar la partida
mtg_game = Game(players=[player1, player2])
mtg_game.start_game()
