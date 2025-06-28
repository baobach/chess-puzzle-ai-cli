# Chess Puzzle AI CLI Wrapper

## Project Description

This project aims to create an interactive Command Line Interface (CLI) tool that launches a chess puzzle for the user to play while an AI agent (or any other long-running command) executes in the background. The puzzle will feature a timer and an announcement that the AI agent is running. Users can continue playing the puzzle until the AI agent completes its task or they choose to exit the puzzle.

## How to Use (Current Stage)

At this stage, the application displays a default chess board in your terminal.

1.  **Ensure Poetry is installed**: If you don't have Poetry, follow the instructions on their official website.

2.  **Install Dependencies**: Navigate to the project's root directory in your terminal and run:
    ```bash
    poetry install
    ```

3.  **Run the Application**: Once dependencies are installed, you can launch the application with:
    ```bash
    poetry run chess-puzzle-ai-cli
    ```

    This will open an interactive chess board in your terminal. You can exit the application by pressing `Ctrl+C`.

Further features, including fetching puzzles and integrating with AI agents, are under development. Check `PLANNING.md` for the detailed development roadmap.