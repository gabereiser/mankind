from models import OrbitalBody, Character, Colony, MarketOrder


class Planet(OrbitalBody):
    def colonize(self, player: Character) -> Colony:
        pass

    def get_colonies(self) -> list[Colony]:
        return self.colonies
