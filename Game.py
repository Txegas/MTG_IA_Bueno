from Player import Player
from StackObject import StackObject
from collections import deque
from Card import Card

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

    def is_game_over(self) -> bool:
        """Verifica si la partida ha terminado."""
        return len(self.players) <= 1

    def execute_turn(self, player: Player):
        """
        Ejecuta las fases del turno para un jugador, permitiendo múltiples acciones en cada fase hasta que el jugador decida continuar.
        
        :param player: Jugador cuyo turno se está jugando
        """
        # DEBUG: No se si esto aqui, deberian resetearse las tierras jugadas por todos os jugadores al principio de cada turno, aunque no sea su turno
        player.reset_turn_lands()

        self.phase_loop(player, "Untap", self.untap_phase)
        self.phase_loop(player, "Upkeep", self.upkeep_phase)
        self.phase_loop(player, "Draw", self.draw_phase)
        self.phase_loop(player, "Precombat Main Phase", lambda p: self.main_phase(p, "Precombat Main Phase"))
        self.phase_loop(player, "Combat", self.combat_phase)
        self.phase_loop(player, "Postcombat Main Phase", lambda p: self.main_phase(p, "Postcombat Main Phase"))
        self.phase_loop(player, "End", self.end_phase)

    def phase_loop(self, player: Player, phase_name: str, phase_function):
        """
        Permite que un jugador realice múltiples acciones en una fase hasta que indique que quiere avanzar.
        
        :param player: Jugador cuyo turno se está jugando
        :param phase_name: Nombre de la fase actual (str)
        :param phase_function: Funcion correspondiente al turno actua
        """
        self.phase = phase_name
        print(f"{player.name} está en la fase de {phase_name}.")

        # Ejecutamos la FUNCION DE FASE DEL TURNO de la fase actual, listadas debajo
        phase_function(player)

        while True:
            self.priority_cycle()
            advance = input(f"{player.name}, ¿quieres pasar a la siguiente fase? (s/n): ")
            if advance.lower() == "s":
                break

###################################### FUNCIONES DE FASE DEL TURNO

    def untap_phase(self, player: Player):
        """Fase de enderezar: Se enderezan todas las permanentes del jugador."""
        self.phase = "Untap"
        self.check_state_based_actions()
    
    def upkeep_phase(self, player: Player):
        """Fase de mantenimiento: Se resuelven habilidades disparadas."""
        self.phase = "Upkeep"
        self.check_state_based_actions()
    
    def draw_phase(self, player: Player):
        """Fase de robo: El jugador roba una carta o pierde si su biblioteca está vacía."""
        self.phase = "Draw"
        player.draw_card()
        self.check_state_based_actions()
        self.check_triggered_abilities("draw", player)
    
    def main_phase(self, player: Player, phase: str):
        """Fase principal: Se pueden jugar tierras, lanzar hechizos y activar habilidades."""
        self.phase = phase
        self.check_state_based_actions()
        self.check_triggered_abilities("main_phase", player)
    
    def combat_phase(self, player: Player):
        """Fase de combate: Se declara ataque y bloqueos."""
        self.phase = "Combat"
        self.check_state_based_actions()
        self.check_triggered_abilities("main_phase", player)
    
    def end_phase(self, player: Player):
        """Fase final: Se resuelven efectos de final de turno y se descartan cartas si es necesario."""
        self.phase = "End"
        self.check_state_based_actions()
        self.check_triggered_abilities("main_phase", player)

######################################

    def priority_cycle(self):
        """Gestiona la prioridad entre los jugadores para jugar hechizos y habilidades."""
        print(f"Se ha activado el ciclo de prioridad en la fase {self.phase}.")

        # Rota la prioridad
        players_in_priority_order = self.players[self.turn_player_index:] + self.players[:self.turn_player_index]
        
        while True:
            passed_players = 0
            for player in players_in_priority_order:
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
        """
        Permite a un jugador jugar un hechizo o activar una habilidad si tiene suficiente maná y cumple las restricciones del juego.
        
        :param player: Jugador con la prioridad
        """
        # Si el jugador no tiene cartas en la mano ni habilidades activables, no puede hacer nada
        if not player.hand and not any(card.activated_abilities for card in player.battlefield):
            return None

        while True:
            response = input(f"{player.name}, ¿quieres jugar un hechizo o activar una habilidad? (h/a/n): ")

            if response.lower() == 'h':

                # Si e jugador quiere lanzar un hechizo, listamos las cartas de su mano y las mostramos como opciones
                for i, card in enumerate(player.hand):
                    print(f"{i+1}. {card.name} - {card.card_types}")
                choice = input(f"Selecciona una carta para jugar (1-{len(player.hand)}): ")
                
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(player.hand):
                        card_to_play = player.hand[index]

                        # Primero, verificar si el jugador tiene suficiente maná
                        if not player.can_pay_mana(card_to_play.mana_cost):
                            print(f"{player.name} no tiene suficiente maná para jugar {card_to_play.name}.")
                            continue  # Volver a preguntar al jugador

                        # Manejo especial para tierras
                        if "Land" in card_to_play.card_types:
                            return self.play_land(player, card_to_play)

                        # Verificamos si la carta tiene una función específica
                        play_function = getattr(self, f"play_{card_to_play.name.replace(' ', '_').lower()}", None)
                        if play_function:
                            return play_function(player, card_to_play)
                        
                        print(f"No hay lógica específica implementada para {card_to_play.name}. No puede jugarse.")
                        continue  # Volvemos a preguntar

                    # Si el jugador introduce un numero fuera del rango de opciones, le volvemos a preguntar
                    else:
                        continue
                
                # Si el jugador introduce algo que no sea un numero, le volvemos a preguntar
                else:
                    continue

            elif response.lower() == 'a':
                available_cards = [card for card in player.battlefield if card.activated_abilities and not card.is_tapped]

                if not available_cards:
                    print("No hay cartas con habilidades activadas disponibles.")
                    continue  # Volvemos a preguntar

                for i, card in enumerate(available_cards):
                    print(f"{i+1}. {card.name} - {card.activated_abilities}")

                ability_choice = input(f"Selecciona una habilidad para activar (1-{len(available_cards)}): ")

                if ability_choice.isdigit():
                    index = int(ability_choice) - 1
                    if 0 <= index < len(available_cards):
                        selected_card = available_cards[index]
                        ability = selected_card.activated_abilities[0]  # Asumiendo que tiene una sola habilidad activada
                        print(f"{player.name} activa {ability} de {selected_card.name}.")
                        return StackObject(card=selected_card, controller=player, ability=ability)

            elif response.lower() == 'n':
                return None  # Solo en este caso se permite que la prioridad pase al siguiente jugador

            else:
                print("Entrada no válida. Debes seleccionar 'h', 'a' o 'n'.")

    def play_land(self, player: Player, card: Card):
        """Permite a un jugador jugar una tierra, respetando la restricción de una por turno."""
        print(f"{player.name} intenta jugar {card.name}.")
        
        # Verificar si el jugador puede jugar la carta
        if player.can_play_card(card, self.phase):
            player.hand.remove(card)
            player.battlefield.append(card)
            card.controller = player  # Asignamos el controlador
            player.lands_played_this_turn += 1  # Marcamos que jugó una tierra
            print(f"{player.name} juega {card.name}.")
            return None  # Las tierras no van al stack

        print(f"{player.name} no puede jugar {card.name}.")
        return None
    
    def select_target(self, player: Player, valid_types: list = ["Player", "Creature", "Planeswalker"]):
        """Permite seleccionar un objetivo de los tipos válidos especificados."""
        valid_targets = []

        if "Player" in valid_types:
            valid_targets.extend(self.players)  # Agregar jugadores si es un objetivo válido
        if "Creature" in valid_types or "Planeswalker" in valid_types:
            for p in self.players:
                valid_targets.extend([card for card in p.battlefield if any(t in valid_types for t in card.card_types)])

        if not valid_targets:
            print("No hay objetivos válidos disponibles.")
            return None

        print("Selecciona un objetivo:")
        for i, target in enumerate(valid_targets):
            if isinstance(target, Player):
                print(f"{i+1}. {target.name} (Jugador)")
            else:
                print(f"{i+1}. {target.name} (Criatura de {target.controller.name})")

        choice = input(f"Selecciona un objetivo (1-{len(valid_targets)}): ")
        
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(valid_targets):
                return valid_targets[index]

        print("Selección inválida.")
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

    def check_triggered_abilities(self, event: str, player: Player, target: Player = None):
        """Verifica si hay habilidades disparadas debido a un evento y las coloca en la pila."""
        for p in self.players:
            for card in p.battlefield:
                if event in card.triggered_abilities:
                    ability = card.triggered_abilities[event]
                    print(f"{card.name} de {p.name} se dispara debido a {event}.")
                    self.stack.append(StackObject(card=card, controller=p, target=target, ability=ability))
    
    def resolve_stack(self):
        """Resuelve los hechizos y habilidades en la pila."""
        print("Resolviendo la pila...")
        while self.stack:
            action = self.stack.pop()
            action.resolve()
            if action.card.passive_effects:
                self.apply_passive_effects(action.controller, action.card)
        self.check_state_based_actions()

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
    

############################################### CARTAS:

    def play_lightning_bolt(self, player: Player, card: Card):
        """
        Instant. Deal 3 damage to any target.
        """
    
        # Permitimos seleccionar cualquier objetivo que pueda recibir daño
        target = self.select_target(player, valid_types=["Player", "Creature", "Planeswalker"])
        if not target:
            print("No se ha seleccionado un objetivo válido.")
            return None  # No se juega la carta si no tiene target válido

        if player.can_play_card(card, self.phase) and player.can_pay_mana(card.mana_cost):
            player.pay_mana(card.mana_cost)
            player.hand.remove(card)
            return StackObject(card=card, controller=player, target=target) # Metemos el hechizo al stack
        
        return None
