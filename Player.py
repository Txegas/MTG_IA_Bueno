from Card import Card

class Player:
    def __init__(self, name: str, deck: list, life_total: int = 40, is_bot: bool = False):
        """
        Representa a un jugador de Magic: The Gathering.
        
        :param name: Nombre del jugador
        :param deck: Lista de objetos de tipo Card que conforman su biblioteca (mazo)
        :param life_total: Total de vidas del jugador (40 en Commander por defecto)
        :param is_bot: Indica si el jugador es un bot o un jugador real
        """
        self.name = name
        self.library = deck  # Biblioteca del jugador (mazo)
        self.hand = []  # Cartas en la mano del jugador
        self.graveyard = []  # Cementerio
        self.battlefield = []  # Cartas en el campo de batalla
        self.exile = []  # Cartas en la zona de exilio
        self.command_zone = []  # Zona del comandante (solo para commander)
        self.life_total = life_total  # Puntos de vida
        self.is_bot = is_bot  # Indica si el jugador es un bot
        self.mana_pool = {"R": 0, "G": 0, "W": 0, "B": 0, "U": 0, "C": 0, "N": 0}  # Reserva de maná disponible
        self.counters = {}  # Contadores en el jugador
        self.turn_priority = False  # Indica si el jugador tiene la prioridad en el turno actual
        self.lands_played_this_turn = 0  # Contador de tierras jugadas este turno

    def reset_turn_lands(self):
        """Resetea el contador de tierras jugadas al inicio de cada turno."""
        self.lands_played_this_turn = 0
        
    def draw_card(self, num: int = 1):
        """Robar cartas de la biblioteca."""
        for _ in range(num):
            if self.library:
                self.hand.append(self.library.pop(0))
            else:
                print(f"{self.name} intenta robar una carta, pero su biblioteca está vacía.")
                # En reglas oficiales, si un jugador intenta robar de un mazo vacío, pierde el juego
    
    def play_card(self, card, game_phase: str):
        """Jugar una carta de la mano si se cumplen las reglas del juego."""

        if "Land" in card.card_types and self.lands_played_this_turn >= 1:
            print(f"{self.name} ya ha jugado una tierra este turno y no puede jugar otra.")
            return  # Evita que la tierra sea jugada
    
        if card in self.hand and self.can_play_card(card, game_phase) and self.can_pay_mana(card.mana_cost):
            self.hand.remove(card)
            if "Land" in card.card_types:
                self.lands_played_this_turn += 1
            self.pay_mana(card.mana_cost)
            print(f"{self.name} juega {card.name}.")
        else:
            print(f"{self.name} no puede jugar {card.name}.")

    def can_play_card(self, card, game_phase: str) -> bool:
        """Verifica si el jugador puede jugar una carta dadas las reglas del juego."""
        if "Land" in card.card_types:
            if self.lands_played_this_turn >= 1:
                print(f"{self.name} ya ha jugado una tierra este turno y no puede jugar otra.")
                return False
        
        if "Instant" not in card.card_types and "Flash" not in card.keywords:
            if game_phase not in ["Precombat Main Phase", "Postcombat Main Phase"]:
                print(f"{self.name} solo puede jugar {card.name} en la fase principal.")
                return False
            
        return True
    
    def can_pay_mana(self, mana_cost: dict) -> bool:
        """Verifica si el jugador tiene suficiente maná para pagar el coste de una carta."""
        for color, amount in mana_cost.items():
            if self.mana_pool.get(color, 0) < amount:
                return False
        return True
    
    def pay_mana(self, mana_cost: dict):
        """Reduce el maná de la reserva del jugador según el coste de la carta."""
        for color, amount in mana_cost.items():
            self.mana_pool[color] -= amount
    
    def gain_life(self, amount: int):
        """Aumenta la vida del jugador."""
        self.life_total += amount
    
    def lose_life(self, amount: int):
        """Reduce la vida del jugador."""
        self.life_total -= amount
        if self.life_total <= 0:
            print(f"{self.name} ha perdido la partida.")
    
    def add_mana(self, color: str, amount: int):
        """Agrega maná a la reserva del jugador."""
        if color in self.mana_pool:
            self.mana_pool[color] += amount
        else:
            print(f"Color de maná inválido: {color}")
    
    def exile_card(self, card: Card):
        """Exilia una carta desde cualquier zona del juego."""
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.battlefield:
            self.battlefield.remove(card)
        elif card in self.graveyard:
            self.graveyard.remove(card)
        self.exile.append(card)
        print(f"{card.name} ha sido exiliada por {self.name}.")
