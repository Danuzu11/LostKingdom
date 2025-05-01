import settings
from src.LostKindom import LostKindom

if __name__ == "__main__":
    game = LostKindom(
        "LostKindom",
        settings.WINDOW_WIDTH,
        settings.WINDOW_HEIGHT,
        settings.VIRTUAL_WIDTH,
        settings.VIRTUAL_HEIGHT,
    )
    game.exec()
