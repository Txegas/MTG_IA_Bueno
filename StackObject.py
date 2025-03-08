from Card import Card
from Player import Player

class StackObject:
    def __init__(self, card: Card, controller: Player, target: Player = None):
        """
        Representa un objeto en la pila (hechizo o habilidad activada).
        
        :param card: La carta asociada al hechizo o habilidad.
        :param controller: El jugador que lanzó el hechizo o activó la habilidad.
        :param target: (Opcional) El objetivo del hechizo o habilidad.
        """
        self.card = card
        self.controller = controller
        self.target = target
    
    def resolve(self):
        """Resuelve el efecto del hechizo o habilidad."""
        print(f"Resolviendo {self.card.name} lanzado por {self.controller.name}.")
        if self.card.name == "Lightning Bolt":
            if self.target:
                self.target.lose_life(3)
                print(f"{self.target.name} recibe 3 puntos de daño.")
        elif self.card.name == "Llanowar Elves":
            self.controller.battlefield.append(self.card)
            print(f"{self.controller.name} pone {self.card.name} en el campo de batalla.")
        else:
            print(f"El efecto de {self.card.name} aún no está implementado.")
