# Precision Drive Golf

A retro-style golf game focusing on precision control and timing. Guide your golf ball through the course using air control to achieve a hole-in-one!

## Game Description

Precision Drive Golf is a unique take on the traditional golf game. Rather than just setting angles and power, you'll actively control your ball's flight path after launching
it from the tee. The objective is to get the ball into the hole in the shortest time possible with precise controls.

### Features

- Retro-style 2D graphics with textured grass
- Unique flight control mechanics
- Power meter for initial swing
- Time tracking for speedrun challenges
- Distance measurement in meters
- Mid-air ball control using arrow keys or WASD

## Controls

- **SPACE**: Hold to charge your swing power, release to launch
- **LEFT/A**: Move the ball left during flight
- **RIGHT/D**: Move the ball right during flight
- **UP/W**: Add lift to keep the ball airborne
- **DOWN/S**: Drop the ball faster
- **ENTER**: Start game / Retry after landing

## Game Mechanics

- **Power Meter**: Controls initial velocity and height of your shot
- **Drift Momentum**: The ball maintains some of its horizontal momentum
- **Air Control**: Use keys to guide your ball while it's in the air
- **Time Challenge**: Try to get to the hole in the fastest time
- **Distance Feedback**: See how close you got to the hole

## Installation

### Requirements

- Python 3.x
- Pygame library

### Setup

1. Make sure you have Python installed on your system
2. Install Pygame using pip:
   ```
   pip install pygame
   ```
3. Download `golf_game.py`
4. Run the game:
   ```
   python3 golf_game.py
   ```

## Game Strategy

- Find the right balance between initial power and in-flight controls
- Use short bursts of directional control rather than holding keys
- Master the drift mechanics to make precise adjustments
- Keep the ball airborne longer with well-timed UP/W presses
- Practice for faster completion times

## Development

This game was created using Grok3 and Pygame and demonstrates concepts such as:
- Game state management
- Physics simulation (velocity, momentum)
- User input handling
- Timer functionality
- Collision detection

## Future Enhancements

- Multiple holes with different challenges
- Wind effects
- Obstacles like trees and water hazards
- Multiplayer mode
- Leaderboard for best times

## Credits

Developed as a mini-game project to demonstrate game physics and real-time control mechanics.

## License

[MIT License](https://opensource.org/licenses/MIT)
