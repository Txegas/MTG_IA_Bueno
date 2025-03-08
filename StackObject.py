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
    
    def resolve(self):
        """Resuelve el efecto del hechizo o habilidad."""
        if self.ability:
            print(f"Resolviendo habilidad activada de {self.card.name}: {self.ability}.")
            # HABILIDADES DE MANA:
            if self.ability == "{T}: Add {G}":
                self.controller.add_mana("G", 1)
                print(f"{self.controller.name} agrega 1 Maná verde a su reserva de maná.")
            else:
                print(f"Efecto de habilidad activada '{self.ability}' aún no implementado.")
        else:
            print(f"Resolviendo {self.card.name} lanzado por {self.controller.name}.")
            if self.card.name == "Lightning Bolt":
                if self.target:
                    self.target.lose_life(3)
                    print(f"{self.target.name} recibe 3 puntos de daño.")
            elif "Creature" or "enchantment" in self.card.card_types:
                self.controller.battlefield.append(self.card)
                print(f"{self.controller.name} pone {self.card.name} en el campo de batalla.")
            else:
                print(f"El efecto de {self.card.name} aún no está implementado.")
