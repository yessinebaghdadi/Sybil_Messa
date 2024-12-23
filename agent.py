from enum import Enum
from mesa import Agent
from wsn_message import WSNMessageType as MT  # Enumération des types de messages

# États possibles pour un agent
class State(Enum):
    NORMAL = "Normal"
    SYBIL = "Sybil"

# Classe de message utilisée pour l'attaque Sybil
class SybilMessage:
    def __init__(self, message_type, source, destination, data):
        self.type = message_type
        self.source = source
        self.destination = destination
        self.data = data

# Classe représentant un agent dans le réseau
class WSNAgent(Agent):
    def __init__(self, unique_id, model, state=State.NORMAL, sybil_identities=0):
        super().__init__(unique_id, model)
        self.state = state
        self.sybil_identities = [f"Sybil_{unique_id}_{i}" for i in range(sybil_identities)] if state == State.SYBIL else []
        self.messages_sent = []
        self.messages_received = []

    def send_message(self, destination, message_type, data):
        """Envoie un message à un autre agent."""
        message = SybilMessage(message_type, self.unique_id, destination.unique_id, data)
        self.model.messages.append(message)
        self.messages_sent.append(message)

    def receive_message(self, message):
        """Ajoute un message reçu à la liste des messages."""
        if message.destination == self.unique_id:
            self.messages_received.append(message)

    def process_messages(self):
        """Traite les messages reçus pour détecter ou influencer d'autres agents."""
        for message in self.messages_received:
            if self.state == State.SYBIL:
                print(f"[SYBIL] {self.unique_id} traite un message de {message.source}")
            elif self.state == State.NORMAL and message.source in self.sybil_identities:
                print(f"[NORMAL] {self.unique_id} détecte une activité Sybil de {message.source}")

    def step(self):
        """Étape de simulation."""
        # Traiter les messages reçus
        self.process_messages()

        # Si l'agent est Sybil, envoyer des messages malveillants
        if self.state == State.SYBIL:
            for neighbor in self.model.grid.get_neighbors(self.pos, include_center=False):
                # Envoi d'un message d'annonce falsifié
                self.send_message(neighbor, MT.Advertisement, 0)

        # Réinitialiser les messages reçus pour l'étape suivante
        self.messages_received = []
