from Card import Card
from Player import Player
from Game import Game

from Card import Card
from Player import Player
from Game import Game

def create_test_deck():
    """Crea un mazo de prueba con cartas básicas, incluyendo habilidades pasivas."""
    return [
        Card(
            name="Llanowar Elves", 
            mana_cost={}, 
            card_types=["Creature"], 
            subtypes=["Elf", "Druid"], 
            text="{T}: Add {G}.", 
            power=1, 
            toughness=1,
            activated_abilities=["{T}: Add {G}"]
        ),
        Card(
            name="Glorious Anthem", 
            mana_cost={}, 
            card_types=["Enchantment"], 
            subtypes=[], 
            text="Las criaturas que controlas obtienen +1/+1.", 
            passive_effects={"buff": {"power": 1, "toughness": 1}}
        ),
        Card(
            name="Vanquisher's Banner", 
            mana_cost={}, 
            card_types=["Artifact"], 
            subtypes=[], 
            text="Las criaturas de un tipo elegido obtienen +1/+1.", 
            passive_effects={"buff": {"power": 1, "toughness": 1}}
        ),
        Card(
            name="Lightning Bolt", 
            mana_cost={}, 
            card_types=["Instant"], 
            subtypes=[], 
            text="Deal 3 damage to any target."
        )
    ] * 15  # Mazo de prueba con 60 cartas en total

# Crear jugadores
player1 = Player(name="Jugador 1", deck=create_test_deck())
player2 = Player(name="Jugador 2", deck=create_test_deck())

# Iniciar la partida
mtg_game = Game(players=[player1, player2])
mtg_game.start_game()
