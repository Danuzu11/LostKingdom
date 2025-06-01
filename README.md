# Lost Kingdom

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

## 🎯 Core Systems

### Player System (`Player.py`)
- Dynamic movement system
- Combat mechanics with attack animations
- Health and damage system
- Knockback mechanics
- State-based animation system
- Collision detection
- System of combo attacks

### Enemy System (`Enemy.py`)
- Advanced AI behavior
- Multiple enemy types:
  - Golem
  - MechaGolem
  - Executoner
  - NightBorne
  - Minotaur
- Individual attack patterns
- Health system
- Death animations
- Detection ranges
- Pursuit mechanics
- Grown detection

### Map System (`TileMap.py`)
- Tiled map integration
- Collision mapping
- Object placement
- Layer management
- Scale factor handling

### Camera System (`Camera.py`)
- Smooth player tracking
- Viewport management
- World boundary handling
- Dynamic positioning

### Animation System (`AnimatedItem.py`)
- Sprite animation management
- Decorative elements:
  - Torches
  - Fireplaces
  - Keys
  - Castle torches
- Frame-based animation system

### Utility Systems
- `globalUtilsFunctions.py`: Animation extraction and sprite management and auxiliar functions
- `QuadTree.py`: Spatial partitioning for optimization to limit the collision detection analysis in a reduced manner

## 🎮 Game States

### State Management (`states/`)
- `PlayState`: Main gameplay
- `MenuState`: Main menu interface
- `PauseState`: Game pause functionality
- `VideoState`: Intro menu scene
- `GameOverState`: End game screen
- `IntroState`: Game introduction
- `OutroState`: Game conclusion

## 🎯 Features

### Combat System
- Dynamic attack animations
- Hit detection
- Knockback mechanics
- Invulnerability frames
- Multiple attack patterns

### Enemy AI
- Pathfinding
- Attack patterns
- Detection ranges
- Pursuit mechanics
- State-based behavior

### Interactive Elements
- Key and door system
- Animated decorations
- Environmental effects
- Collectible items

### Audio System
- Background music
- Sound effects:
  - Combat sounds
  - Environmental effects
  - Enemy sounds
  - Menu sounds
  - Death sounds

## 🎮 Controls

- **Movement**:
  - `←`: Move left
  - `→`: Move right
  - `Space`: Jump
  - `X`: Attack
  - `F`: Special action (For now only open doors)
  - `P`: Pause game
  - `ESC`: Exit

## 🗺️ Levels

- `intro`: Introduction level
- `level1`: Castle level
- `roomboss`: Boss room
  
## 📁 Project Structure
src/

    ├── init.py
    ├── LostKindom.py # Main game file and entry point
    ├── Player.py # Player character implementation
    │ ├── Movement system
    │ ├── Combat mechanics
    │ ├── Animation states
    │ └── Health system
    │
    ├── Enemy.py # Enemy AI and behavior
    │ ├── AI pathfinding
    │ ├── Attack patterns
    │ ├── State management
    │ └── Collision detection
    │
    ├── TileMap.py # Tile map system
    │ ├── Map loading
    │ ├── Tile rendering
    │ └── Collision mapping
    │
    ├── Camera.py # Camera system
    │ ├── Player tracking
    │ ├── Smooth following
    │ └── Viewport management
    │
    ├── AnimatedItem.py # Interactive items
    │ └── Animation system
    │
    ├── globalUtilsFunctions.py # Utility functions
    │ ├── Animation extraction
    │ ├── Sprite management
    │ └── Helper functions
    │
    ├── definitions/ # Game definitions
    │ ├── enemies.py # Enemy configurations
    │ │ ├── Stats
    │ │ ├── Behaviors
    │ │ └── Properties
    │ └── [Other definitions]
    │
    └── states/ # Game state management
    ├── init.py
    ├── PlayState.py # Main gameplay state
    ├── MenuState.py # Main menu
    ├── PauseState.py # Pause menu
    ├── VideoState.py # Cutscene handling
    └── GameOverState.py # Game over screen

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
python src/main.py
```

## 🎨 Extra System Features

### Collision System
- World collision detection
- Knockback system
- Attack collisions
- Ground detection
- Object interaction

### Animation System
- Movement animations (idle, run, jump)
- Attack animations
- Death animations
- Visual effects and animated decorations

## 🐛 Troubleshooting

### Common Issues
1. **PNG sRGB Profile Warning**:
   - Common warning that doesn't affect functionality
   - Can be ignored or fixed by processing images

2. **Performance Issues**:
   - Ensure you have the latest dependency versions
   - Check for background processes
   - Verify system requirements

## 📝 License

 - In progress ... :D

## 🎮 Game Development Notes

- The game uses a state-based system for different screens
- Implements a sprite-based animation system
- Features a custom collision system
- Includes a dynamic camera system
- Uses a tile-based world design
- Implements enemy AI with different behaviors
- Features a key and door interaction system
- Includes animated decorations and environmental effects
