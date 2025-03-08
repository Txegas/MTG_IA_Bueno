
# Definimos constantes con las opciones válidas para algunos parámetros
VALID_MANA_TYPES = ["R", "G", "W", "B", "U", "C", "N"]
VALID_CARD_TYPES = ["Creature", "Artifact", "Enchantment", "Instant", "Sorcery", "Land", "Planeswalker", "Battle"]
VALID_RARITIES = ["Common", "Uncommon", "Rare", "Mythic Rare"]
VALID_KEYWORDS = ["Flying", "Trample", "Deathtouch", "Lifelink", "Hexproof", "Haste", "Vigilance", "Menace", "Defender", "Double strike", "First strike", "Enchant", "Equip", "Flash", "Indestructible", "Protection", "Prowess", "Reach", "Vigilance", "Absorb", "Adapt", "Affinity", "Afterlife", "Aftermath", "Amplify", "Annihilator", "Ascend", "Aura swap", "Bands with other", "Battle cry", "Bestow", "Bolster", "Bloodthirst", "Bushido", "Buyback", "Cascade", "Champion", "Changeling", "Cipher", "Clash", "Conspire", "Convoke", "Crew", "Cumulative upkeep", "Cycling", "Dash", "Daybound", "Nightbound", "Delve", "Detain", "Devour", "Dredge", "Echo", "Embalm", "Emerge", "Entwine", "Epic", "Evolve", "Evoke", "Exalted", "Exert", "Exploit", "Explore", "Extort", "Fabricate", "Fading", "Fateseal", "Flanking", "Flashback", "Flip", "Forecast", "Foretell", "Fortify", "Frenzy", "Graft", "Gravestorm", "Haunt", "Hideaway", "Horsemanship", "Infect", "Jump-start", "Kicker", "Level up", "Living weapon", "Madness", "Manifest", "Meld", "Mentor", "Miracle", "Modular", "Monstrosity", "Morph", "Multikicker", "Mutate", "Ninjutsu", "Offering", "Overload", "Persist", "Plot", "Poisonous", "Populate", "Proliferate", "Provoke", "Prowl", "Radiation", "Rampage", "Rebound", "Recover", "Reinforce", "Renown", "Replicate", "Retrace", "Riot", "Ripple", "Scavenge", "Shadow", "Soulbond", "Soulshift", "Spectacle", "Splice", "Split second", "Storm", "Sunburst", "Support", "Suspend", "Transfigure", "Transform", "Transmute", "Typecycling", "Umbra armor", "Undying", "Unearth", "Unleash", "Vanishing", "Ward", "Wither", "Addendum", "Battalion", "Bloodrush", "Channel", "Chroma", "Domain", "Enrage", "Fateful hour", "Ferocious", "Grandeur", "Hellbent", "Heroic", "Imprint", "Join forces", "Kinship", "Landfall", "Metalcraft", "Morbid", "Radiance", "Raid", "Rally", "Sweep", "Threshold", "Undergrowth", "Banding", "Bury", "Fear", "Intimidate", "Landhome", "Landwalk", "Phasing", "Regenerate", "Shroud", "Substance"]
VALID_KEYWORD_ACTIONS = ["Attach", "Counter", "Exile", "Fight", "Mill", "Sacrifice", "Scry", "Tap", "Untap", "Surveil"]
VALID_FRAME_EFFECTS = ["Retro Frame", "Full Art", "Borderless", "Etched Foil"]


class Card:
    def __init__(self, name: str, mana_cost: dict, card_types: list, subtypes: list, text: str,
                 power: int = None, toughness: int = None, loyalty: int = None,
                 keywords: list = None, keyword_actions: list = None, expansion: str = None, rarity: str = None,
                 image: str = None, color_indicator: list = None, expansion_symbol: str = None,
                 collector_number: int = None, flavor_text: str = None, frame_effects: list = None,
                 passive_effects: dict = None, activated_abilities: list = None, triggered_abilities: dict = None, is_tapped = False):
        """
        Clase base para representar una carta de Magic: The Gathering.

        :param name: Nombre de la carta
        :param mana_cost: Coste de maná en un diccionario con claves 'R', 'G', 'W', 'B', 'U', 'C', 'N'
        :param card_types: Lista de tipos de carta (ej. ["Creature", "Artifact"])
        :param subtypes: Lista de subtipos de la carta (ej. ["Elf", "Warrior"])
        :param text: Texto de reglas de la carta
        :param power: Poder de la criatura (None si no aplica)
        :param toughness: Resistencia de la criatura (None si no aplica)
        :param loyalty: Lealtad del planeswalker (None si no aplica)
        :param keywords: Lista de palabras clave (habilidades) de la carta (ej. ["Flying", "Trample"])
        :param expansion: Nombre de la expansión a la que pertenece la carta
        :param rarity: Rareza de la carta (ej. "Common", "Uncommon", "Rare", "Mythic Rare")
        :param image: Ruta o URL de la imagen de la carta
        :param color_indicator: Lista de colores asociados a la carta (ej. ["Red", "Green"])
        :param expansion_symbol: Símbolo de la expansión de la carta
        :param collector_number: Número de coleccionista de la carta en la expansión
        :param flavor_text: Texto de ambientación de la carta
        :param frame_effects: Lista de efectos de marco o estilos alternativos (ej. ["Retro Frame", "Full Art"])
        """

        # Validaciones. Si intentas crear una carta con un tipo de maná, rareza... inválido, el programa lanzará una excepción con un mensaje de error.
        if not all(k in VALID_MANA_TYPES for k in mana_cost.keys()):
            raise ValueError("Mana_cost contiene valores no válidos.")
        if not all(ct in VALID_CARD_TYPES for ct in card_types):
            raise ValueError("Card_type contiene valores no válidos.")
        if rarity and rarity not in VALID_RARITIES:
            raise ValueError("Rarity no válida.")
        if keywords and not all(k in VALID_KEYWORDS for k in keywords):
            raise ValueError("Algunas keywords no son válidas.")
        if keyword_actions and not all(ka in VALID_KEYWORD_ACTIONS for ka in keyword_actions):
            raise ValueError("Algunas keywords_actions no son válidas.")
        if frame_effects and not all(f in VALID_FRAME_EFFECTS for f in frame_effects):
            raise ValueError("Algunos frame_effects no son válidos.")
        
        # Atributos de la clase Card
        self.name = name
        self.mana_cost = mana_cost
        self.card_types = card_types
        self.subtypes = subtypes
        self.text = text
        self.power = power
        self.toughness = toughness
        self.loyalty = loyalty
        self.keywords = keywords if keywords else []
        self.keyword_actions = keyword_actions if keyword_actions else []
        self.expansion = expansion
        self.rarity = rarity
        self.image = image
        self.color_indicator = color_indicator if color_indicator else []
        self.expansion_symbol = expansion_symbol
        self.collector_number = collector_number
        self.flavor_text = flavor_text
        self.frame_effects = frame_effects if frame_effects else []
        self.passive_effects = passive_effects if passive_effects else {}
        self.activated_abilities = activated_abilities if activated_abilities else []
        self.triggered_abilities = triggered_abilities if triggered_abilities else {}
        self.is_tapped = is_tapped

    def __str__(self):
        mana_cost_str = " ".join(f"{k}:{v}" for k, v in self.mana_cost.items() if v > 0)
        types_str = " ".join(self.card_types)
        subtypes_str = " - " + " ".join(self.subtypes) if self.subtypes else ""
        stats = f" ({self.power}/{self.toughness})" if self.power is not None else ""
        stats = f" [Lealtad: {self.loyalty}]" if self.loyalty is not None else stats
        keywords_str = ", ".join(self.keywords) if self.keywords else "Ninguna"
        keyword_actions_str = ", ".join(self.keyword_actions) if self.keyword_actions else "Ninguna"
        expansion_str = f"Expansión: {self.expansion}" if self.expansion else "Expansión desconocida"
        rarity_str = f"Rareza: {self.rarity}" if self.rarity else "Rareza desconocida"
        flavor_text_str = f"\n\"{self.flavor_text}\"" if self.flavor_text else ""
        return (f"{self.name} ({mana_cost_str}) - {types_str}{subtypes_str}{stats}\n"
                f"{self.text}\n"
                f"Habilidades: {keywords_str}\n"
                f"Acciones de palabra clave: {keyword_actions_str}\n"
                f"{expansion_str} | {rarity_str}\n"
                f"Número de coleccionista: {self.collector_number}\n"
                f"Efectos de marco: {', '.join(self.frame_effects)}\n"
                f"Tapped: {self.is_tapped}\n"
                f"{flavor_text_str}")