from Card import Card
from Player import Player

class StackObject:
    def __init__(self, card: Card, controller: Player, target: Player = None, ability: str = None):
        """
        Representa un objeto en la pila (hechizo o habilidad activada).
        
        :param card: La carta asociada al hechizo o habilidad.
        :param controller: El jugador que lanzó el hechizo o activó la habilidad.
        :param target: (Opcional) El objetivo del hechizo o habilidad.
        :param ability: (Opcional) Si el objeto en la pila es una habilidad activada, se almacena aquí.
        """
        self.card = card
        self.controller = controller
        self.target = target
        self.ability = ability

        if self.card.controller is None:
            self.card.controller = controller
    
    def resolve(self):
        """Resuelve el efecto del hechizo o habilidad."""
        if self.ability:
            print(f"Resolviendo habilidad de {self.card.name}: {self.ability}.")

            # Verificar si la habilidad requiere girar ({T}) para activarse
            if "{T}" in self.ability:
                if not self.card.is_tapped:
                    self.card.is_tapped = True
                    print(f"{self.card.name} se gira para activar su habilidad.")
                else:
                    print(f"{self.card.name} ya está girada y no puede activarse nuevamente.")
                    return
            
            # Manejo de habilidades de generación de maná
            if "Add" in self.ability:
                mana_generated = self.ability.split("Add")[-1].strip(" {}.")
                for symbol in mana_generated:
                    if symbol in self.controller.mana_pool:
                        self.controller.add_mana(symbol, 1)
                        print(f"{self.controller.name} agrega 1 maná {symbol} a su reserva.")
            
            else:
                print(f"Efecto de habilidad activada '{self.ability}' aún no implementado.")
        else:
            print(f"Resolviendo {self.card.name} lanzado por {self.controller.name}.")

            #Lightning Bolt
            if self.card.name == "Lightning Bolt":
                if self.target:
                    if isinstance(self.target, Player):
                        self.target.lose_life(3)
                        print(f"{self.target.name} recibe 3 puntos de daño.")
                    elif "Creature" in self.target.card_types:
                        self.target.toughness -= 3
                        print(f"{self.target.name} recibe 3 puntos de daño.")

            # Si la carta es un permanente (criatura, tierra, artefacto, encantamiento), entra al campo de batalla
            elif "Creature" in self.card.card_types or "Land" in self.card.card_types or "Artifact" in self.card.card_types or "Enchantment" in self.card.card_types:
                self.card.controller = self.controller  # Asignamos el controlador al entrar en el campo
                self.controller.battlefield.append(self.card)
                print(f"{self.controller.name} pone {self.card.name} en el campo de batalla.")
            else:
                print(f"El efecto de {self.card.name} aún no está implementado.")
