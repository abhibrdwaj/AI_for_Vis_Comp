```javascript
// script.js

// Player Class
class Player {
  constructor() {
    this.position = { x: 0, y: 0 };
    this.inventory = [];
    this.hasTorch = false;
  }

  move(dx, dy) {
    if (this.position.x + dx >= 0 && this.position.x + dx < 10 && this.position.y + dy >= 0 && this.position.y + dy < 10) {
      this.position.x += dx;
      this.position.y += dy;
    }
  }
}

// Maze Class
class Maze {
  constructor() {
    this.grid = [
      ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
      ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
      ["#", " ", "#", "#", "#", "#", "#", "#", " ", "#"],
      ["#", " ", "#", " ", " ", " ", " ", "#", " ", "#"],
      ["#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
      ["#", " ", "#", " ", "#", " ", " ", "#", " ", "#"],
      ["#", " ", "#", "#", "#", " ", "#", "#", " ", "#"],
      ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
      ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ];
    this.exit = { x: 8, y: 8 };
    this.keyPositions = [{ x: 3, y: 5 }, { x: 5, y: 3 }, { x: 7, y: 7 }];
    this.torchPosition = { x: 1, y: 7 };
  }

  isColliding(player, dx, dy) {
    const newX = player.position.x + dx;
    const newY = player.position.y + dy;
    if (newX >= 0 && newX < 10 && newY >= 0 && newY < 10) {
      return this.grid[newX][newY] === "#";
    }
    return true;
  }

  collectKey(player, keyPosition) {
    const key = this.grid[keyPosition.x][keyPosition.y];
    if (key === " ") {
      player.inventory.push("key");
      this.grid[keyPosition.x][keyPosition.y] = "#";
      return true;
    }
    return false;
  }

  lightTorch(player) {
    player.hasTorch = player.position.x === this.torchPosition.x && player.position.y === this.torchPosition.y;
  }

  checkWin(player) {
    if (
      player.position.x === this.exit.x &&
      player.position.y === this.exit.y
    ) {
      return true;
    }
    return false;
  }
}

// Game Logic
function updateGame() {
  const player = new Player();
  const maze = new Maze();
  const keys = new Array(3); // array of left, right, up, down arrow keys

  document.addEventListener("keydown", (event) => {
    const code = event.code;
    if (code === keys[0]) {
      player.move(-1, 0);
    } else if (code === keys[1]) {
      player.move(1, 0);
    } else if (code === keys[2]) {
      player.move(0, -1);
    } else if (code === keys[3]) {
      player.move(0, 1);
    }

    if (maze.isColliding(player, 0, 0)) {
      console.log("Collision prevented!");
    } else {
      maze.lightTorch(player);
    }

    if (maze.checkWin(player)) {
      console.log("You Win!");
      return;
    }

    for (const keyPosition of maze.keyPositions) {
      if (maze.collectKey(player, keyPosition)) {
        console.log("You collected a key!");
      }
    }

    document.getElementById("player").style.top = `${player.position.y * 30}px`;
    document.getElementById("player").style.left = `${player.position.x * 30}px`;
  });

  document.addEventListener("click", (event) => {
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.cursor.y - rect.top;
    console.log("Clicked treasure box at x:", x, ", y:", y);
  });

  function renderGame() {
    const ctx = document.getElementById("game-canvas").getContext("2d");
    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 10; j++) {
        if (maze.grid[i][j] === "#") {
          ctx.fillStyle = "black";
        } else {
          ctx.fillStyle = "white";
        }
        ctx.fillRect(j * 30, i * 30, 30, 30);
        if (maze.grid[i][j] === "#") {
          ctx.fillStyle = "white";
          ctx.font = "20px Arial";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText("#", j * 30 + 15, i * 30 + 15);
        }
      }
    }
  }

  function playGame() {
    renderGame();
    requestAnimationFrame(playGame);
  }

  playGame();
}

updateGame();
```

This script implements the core game logic for a simple maze game. It uses objects and functions to encapsulate the game mechanics, making the code modular and reusable. The game logic includes:

- Player movement using arrow keys and mouse click for clicking treasure boxes
- Collision detection with the maze walls
- Key collection and win condition
- Torch lighting and win condition

The game state is rendered on a canvas, and the game updates at 60 FPS.

This code can be used as a starting point for your maze game implementation. You can add more features, such as animating the player movement or adding multiple levels, by extending the provided classes and functions.