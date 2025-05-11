# Memories of the Lost Kingdom

A 2D action-adventure game developed with Python and Pygame, featuring dynamic combat, enemy AI, and a rich tile-based world.

## 🎮 About the Game

Memories of the Lost Kingdom is an immersive 2D action-adventure game where players explore a mysterious kingdom filled with challenges and enemies. The game features smooth animations, responsive combat mechanics, and intelligent enemy behavior.

## 🎯 Technologies Used

- **Python**: Core programming language
- **Pygame**: Game development framework
- **Tiled**: Map editor for creating game levels
- **PyTMX**: Python library for loading Tiled maps
- **PyMovie**: Video processing capabilities
- **Gale**: Animation and sprite management

## 🎯 Features

- Dynamic combat system with attack animations and hit detection
- Intelligent enemy AI with pathfinding and attack patterns
- Smooth camera system with player tracking
- Tile-based world design with collision detection
- Animated items and interactive elements
- State-based game management
- Health system and damage mechanics
- Responsive controls and character movement

## �� Project Structure
src/
    ├── init.py
    ├── LostKindom.py           # Main game file and entry point
    ├── Player.py               # Player character implementation
    │ ├── Movement system
    │ ├── Combat mechanics
    │ ├── Animation states
    │ └── Health system
    │
    ├── Enemy.py                # Enemy AI and behavior
    │ ├── AI pathfinding
    │ ├── Attack patterns
    │ ├── State management
    │ └── Collision detection
    │
    ├── TileMap.py              # Tile map system
    │ ├── Map loading
    │ ├── Tile rendering
    │ └── Collision mapping
    │
    ├── Camera.py               # Camera system
    │ ├── Player tracking
    │ ├── Smooth following
    │ └── Viewport management
    │
    ├── AnimatedItem.py         # Interactive items
    │ └── Animation system
    │
    ├── globalUtilsFunctions.py # Utility functions
    │ ├── Animation extraction
    │ ├── Sprite management
    │ └── Helper functions
    │
    ├── definitions/            # Game definitions
    │ ├── enemies.py            # Enemy configurations
    │ │ ├── Stats
    │ │ ├── Behaviors
    │ │ └── Properties
    │ └── [Other definitions]
    │
    └── states/                 # Game state management
    ├── init.py
    ├── PlayState.py            # Main gameplay state
    ├── MenuState.py            # Main menu
    ├── PauseState.py           # Pause menu
    ├── VideoState.py           # Cutscene handling
    └── GameOverState.py        # Game over screen

### Key Components

- **Game States**: Manages different game screens and modes
  - Play State: Main gameplay
  - Menu State: Main menu interface
  - Pause State: Game pause functionality
  - Video State: Cutscene handling
  - Game Over State: End game screen

- **Core Systems**:
  - Player System: Character control and combat
  - Enemy System: AI and behavior patterns
  - Tile System: World building and collision
  - Camera System: View management
  - Animation System: Sprite and effect animations

- **Definitions**:
  - Enemy configurations
  - Game constants
  - System parameters

- **Utilities**:
  - Animation handling
  - Sprite management
  - Helper functions


## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Pygame
- PyTMX
- PyMovie
- Gale

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/memories-of-the-lost-kingdom.git
```

2. Install required dependencies:
```bash
pip install -r requirements.txt

or

pip install pygame pytmx pymovie https://github.com/R3mmurd/Gale/archive/main.zip
```

3. Run the game:
```bash
python src/LostKindom.py
```

## 🎨 Game Development

The game uses Tiled for map creation, allowing for:
- Custom tile layers
- Object placement
- Collision mapping
- Custom properties for game objects

## 🤝 Contributing

Contributions are welcome!...

## 📝 License

This project is licensed...
