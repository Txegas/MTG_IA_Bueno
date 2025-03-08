from Player import Player
from StackObject import StackObject
from collections import deque

class Game:
    def __init__(self, players: list):
        """
        Representa una partida de Magic: The Gathering.
        
        :param players: Lista de objetos Player representando a los jugadores de la partida.
        """
        self.players = players  # Lista de jugadores en la partida
        self.turn_player_index = 0  # Índice del jugador que tiene el turno actual
        self.phase = ""  # Fase actual de la partida
        self.stack = deque()  # Pila para manejar hechizos y habilidades
    
    def start_game(self):
        """Inicializa la partida y comienza el ciclo de turnos."""
        print("La partida ha comenzado!")
        self.starting_hands()
        self.turn_cycle()

    def starting_hands(self):
        """Cada jugador roba su mano inicial (7 cartas)."""
        for player in self.players:
            player.draw_card(7)
            print(f"{player.name} ha robado su mano inicial.")

    def apply_passive_effects(self, player: Player, card):
        """Aplica los efectos pasivos de una carta cuando entra al campo de batalla."""
        if not card.passive_effects:
            return

        for effect, details in card.passive_effects.items():
            if effect == "buff":
                for target in self.players:
                    for creature in target.battlefield:
                        if "Creature" in creature.card_types:
                            creature.power += details.get("power", 0)
                            creature.toughness += details.get("toughness", 0)
                            print(f"{creature.name} obtiene +{details.get('power', 0)}/+{details.get('toughness', 0)} gracias a {card.name}.")

    def turn_cycle(self):
        """Controla el ciclo de turnos de la partida."""
        while not self.is_game_over():
            current_player = self.players[self.turn_player_index]
            print(f"\nEs el turno de {current_player.name}")
            self.execute_turn(current_player)
            self.turn_player_index = (self.turn_player_index + 1) % len(self.players)
    
    def execute_turn(self, player: Player):
        """Ejecuta las fases del turno para un jugador."""
        self.untap_phase(player)
        self.priority_cycle()
        self.upkeep_phase(player)
        self.priority_cycle()
        self.draw_phase(player)
        self.priority_cycle()
        self.main_phase(player, phase="Precombat Main Phase")
        self.priority_cycle()
        self.combat_phase(player)
        self.priority_cycle()
        self.main_phase(player, phase="Postcombat Main Phase")
        self.priority_cycle()
        self.end_phase(player)
        self.priority_cycle()
    
    def untap_phase(self, player: Player):
        """Fase de enderezar: Se enderezan todas las permanentes del jugador."""
        self.phase = "Untap"
        print(f"{player.name} está en la fase de Enderezar.")
    
    def upkeep_phase(self, player: Player):
        """Fase de mantenimiento: Se resuelven habilidades disparadas."""
        self.phase = "Upkeep"
        print(f"{player.name} está en la fase de Mantenimiento.")
    
    def draw_phase(self, player: Player):
        """Fase de robo: El jugador roba una carta o pierde si su biblioteca está vacía."""
        self.phase = "Draw"
        if not player.library:
            print(f"{player.name} intenta robar pero su biblioteca está vacía. {player.name} ha perdido la partida.")
            self.players.remove(player)
        else:
            player.draw_card()
            print(f"{player.name} ha robado una carta.")
        self.check_state_based_actions()
    
    def main_phase(self, player: Player, phase: str):
        """Fase principal: Se pueden jugar tierras, lanzar hechizos y activar habilidades."""
        self.phase = phase
        print(f"{player.name} está en la {phase}.")
        self.check_state_based_actions()
    
    def combat_phase(self, player: Player):
        """Fase de combate: Se declara ataque y bloqueos."""
        self.phase = "Combat"
        print(f"{player.name} está en la fase de combate.")
        self.check_state_based_actions()
    
    def end_phase(self, player: Player):
        """Fase final: Se resuelven efectos de final de turno y se descartan cartas si es necesario."""
        self.phase = "End"
        print(f"{player.name} está en la fase de final de turno.")
        self.check_state_based_actions()
    
    def is_game_over(self) -> bool:
        """Verifica si la partida ha terminado."""
        return len(self.players) <= 1
    
    def priority_cycle(self):
        """Gestiona la prioridad entre los jugadores para jugar hechizos y habilidades."""
        print(f"Se ha activado el ciclo de prioridad en la fase {self.phase}.")
        while True:
            passed_players = 0
            for player in self.players:
                action = self.get_player_action(player)
                if action:
                    self.stack.append(action)
                    if action.ability:
                        print(f"{player.name} ha agregado la habilidad activada ({action.ability}) de {action.card.name} al stack.")
                    else:
                        print(f"{player.name} ha agregado el hechizo {action.card.name} al stack.")
                else:
                    passed_players += 1
            
            if passed_players == len(self.players):
                break  # Si todos pasan, se avanza la fase
        self.resolve_stack()
        self.check_state_based_actions()

    def get_player_action(self, player: Player):
        """Permite a un jugador jugar un hechizo o activar una habilidad si tiene suficiente maná."""
        if not player.hand and not any(card.activated_abilities for card in player.battlefield):
            return None
        
        response = input(f"{player.name}, ¿quieres jugar un hechizo o activar una habilidad? (h/a/n): ")
        if response.lower() == 'h':
            card_to_play = player.hand[0]  # Por ahora, jugamos la primera carta en mano
            if player.can_pay_mana(card_to_play.mana_cost):
                player.pay_mana(card_to_play.mana_cost)
                player.hand.remove(card_to_play)
                return StackObject(card=card_to_play, controller=player)
            else:
                print(f"{player.name} no tiene suficiente maná para jugar {card_to_play.name}.")
        elif response.lower() == 'a':
            for card in player.battlefield:
                if card.activated_abilities:
                    print(f"Habilidades de {card.name}: {card.activated_abilities}")
                    ability_choice = input(f"Selecciona una habilidad de {card.name} para activar (1-{len(card.activated_abilities)}): ")
                    if ability_choice.isdigit():
                        ability_index = int(ability_choice) - 1
                        if 0 <= ability_index < len(card.activated_abilities):
                            ability = card.activated_abilities[ability_index]
                            print(f"{player.name} activa {ability} de {card.name}.")
                            return StackObject(card=card, controller=player, ability=ability)  # Se activa en la pila
        return None
    
    def check_state_based_actions(self):
        """Verifica y aplica las reglas de State-Based Actions (SBAs)."""
        for player in self.players:
            if player.life_total <= 0:
                print(f"{player.name} ha perdido la partida por tener 0 o menos vidas.")
                self.players.remove(player)

            for card in player.battlefield:
                if card.power is not None and card.toughness is not None and card.toughness <= 0:
                    print(f"{card.name} ha sido destruida por tener 0 o menos de resistencia.")
                    player.battlefield.remove(card)
                    player.graveyard.append(card)
    
    def resolve_stack(self):
        """Resuelve los hechizos y habilidades en la pila."""
        print("Resolviendo la pila...")
        while self.stack:
            action = self.stack.pop()
            action.resolve()
            if action.card.passive_effects:
                self.apply_passive_effects(action.controller, action.card)
        self.check_state_based_actions()
