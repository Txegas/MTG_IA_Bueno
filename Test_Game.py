from Card import Card
from Player import Player
from Game import Game

from Card import Card
from Player import Player
from Game import Game

def create_test_deck():
    """Crea un mazo de prueba con tierras rojas y verdes, Llanowar Elves y Lightning Bolt."""
    return [
        Card(
            name="Mountain", 
            mana_cost={}, 
            card_types=["Land"], 
            subtypes=["Mountain"], 
            text="{T}: Add {R}.",
            activated_abilities=["{T}: Add {R}"]
        ),
        Card(
            name="Forest", 
            mana_cost={}, 
            card_types=["Land"], 
            subtypes=["Forest"], 
            text="{T}: Add {G}.",
            activated_abilities=["{T}: Add {G}"]
        ),
        Card(
            name="Llanowar Elves", 
            mana_cost={"G": 1}, 
            card_types=["Creature"], 
            subtypes=["Elf", "Druid"], 
            text="{T}: Add {G}.", 
            power=1, 
            toughness=1,
            activated_abilities=["{T}: Add {G}"]
        ),
        Card(
            name="Lightning Bolt", 
            mana_cost={"R": 1}, 
            card_types=["Instant"], 
            subtypes=[], 
            text="Deal 3 damage to any target."
        )
    ] * 15  # Mazo con 60 cartas en total

# Crear jugadores
player1 = Player(name="Jugador 1", deck=create_test_deck())
player2 = Player(name="Jugador 2", deck=create_test_deck())

# Iniciar la partida
mtg_game = Game(players=[player1, player2])
mtg_game.start_game()
