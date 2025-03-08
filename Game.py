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
    
    def main_phase(self, player: Player, phase: str):
        """Fase principal: Se pueden jugar tierras, lanzar hechizos y activar habilidades."""
        self.phase = phase
        print(f"{player.name} está en la {phase}.")
    
    def combat_phase(self, player: Player):
        """Fase de combate: Se declara ataque y bloqueos."""
        self.phase = "Combat"
        print(f"{player.name} está en la fase de combate.")
    
    def end_phase(self, player: Player):
        """Fase final: Se resuelven efectos de final de turno y se descartan cartas si es necesario."""
        self.phase = "End"
        print(f"{player.name} está en la fase de final de turno.")
    
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
                    print(f"{player.name} ha agregado {action.card.name} al stack.")
                else:
                    passed_players += 1
            
            if passed_players == len(self.players):
                break  # Si todos pasan, se avanza la fase

        self.resolve_stack()
    
    def get_player_action(self, player: Player):
        """Permite a un jugador jugar un hechizo de su mano si tiene suficiente maná."""
        if not player.hand:
            return None
        
        response = input(f"{player.name}, ¿quieres jugar un hechizo o activar una habilidad? (s/n): ")
        if response.lower() == 's':
            card_to_play = player.hand[0]  # Por ahora, jugamos la primera carta en mano
            if player.can_pay_mana(card_to_play.mana_cost):
                player.pay_mana(card_to_play.mana_cost)
                player.hand.remove(card_to_play)
                return StackObject(card=card_to_play, controller=player)
            else:
                print(f"{player.name} no tiene suficiente maná para jugar {card_to_play.name}.")
        return None
    
    def resolve_stack(self):
        """Resuelve los hechizos y habilidades en la pila."""
        print("Resolviendo la pila...")
        while self.stack:
            action = self.stack.pop()
            action.resolve()