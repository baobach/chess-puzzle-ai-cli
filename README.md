# Chess Puzzle AI CLI Wrapper

## Project Objective

To create an interactive Command Line Interface (CLI) tool that launches a chess puzzle for the user to play while an AI agent (or any other long-running command) executes in the background. The puzzle will feature a timer and an announcement that the AI agent is running. Users can continue playing the puzzle until the AI agent completes its task or they choose to exit the puzzle.

## High-Level Vision & Architecture

The core of this application will be a **wrapper CLI**. Instead of directly running their AI agent command, the user will pass it as an argument to our tool.

**Workflow:**

1.  **User Input**: `chess-puzzle-cli --command "your-ai-agent-command --with --args"`
2.  **Tool Initialization**:
    *   The tool launches the specified AI agent command as a **background process**.
    *   It stores the Process ID (PID) of the background agent.
3.  **Puzzle Launch**: While the AI agent runs, the interactive chess puzzle is launched in the **foreground**.
    *   The UI will display a chessboard, a timer, and a status message indicating the AI agent's activity.
4.  **Termination Conditions**: The chess puzzle loop will continuously monitor:
    *   The completion status of the background AI agent process.
    *   User input to manually quit the puzzle (e.g., by typing 'q').
5.  **Cleanup**: Upon meeting either termination condition, the tool will gracefully exit, ensuring the terminal is restored to its original state.

This wrapper approach provides a robust and self-contained solution for managing the lifecycle of the wrapped AI agent.

## Proposed Technology Stack

**Language**: Python 3

**Key Libraries:**

*   [python-chess](https://github.com/niklasf/python-chess): For handling all chess-related logic, board states, and move validation.
*   [rich](https://github.com/Textualize/rich): For creating a visually appealing and interactive terminal user interface, including rendering the chessboard.
*   [requests](https://github.com/psf/requests): For making HTTP requests to fetch chess puzzles from an external API.
*   [subprocess](https://docs.python.org/3/library/subprocess.html) (built-in Python module): For managing and monitoring the background AI agent process.
*   [argparse](https://docs.python.org/3/library/argparse.html) (built-in Python module): For parsing command-line arguments.

**Puzzle Source**: [Lichess API](https://lichess.org/api) (for fetching daily or themed chess puzzles).

## Phased Implementation Plan

We will adopt a block-by-block development approach, ensuring a functional component at the end of each phase.

### Phase 1: The Standalone Chess Puzzle
**Goal**: Develop a fully functional, interactive chess puzzle CLI tool, independent of the AI agent wrapper.

1.  **Project Setup**: Initialize a Python project with `pyproject.toml` to manage dependencies (`rich`, `python-chess`, `requests`).
2.  **Fetch Puzzle**: Implement a function to retrieve a chess puzzle (FEN, moves) from the Lichess API.
3.  **Display Board**: Create a function using `rich` to render a colorized chessboard in the terminal.
4.  **Interactive Game Loop**: Implement the core game loop, handling user moves, validating them against the puzzle solution, providing feedback, and updating the board until the puzzle is solved or the user quits.

### Phase 2: The AI Agent Wrapper Integration
**Goal**: Integrate the standalone chess puzzle into the wrapper that manages a background process.

1.  **CLI Entrypoint**: Develop the main script to accept the `--command` argument using `argparse`.
2.  **Process Management**: Implement logic to execute the provided command as a background process using `subprocess` and monitor its status.
3.  **Integrate Game Loop**: Launch the background command first, then start the chess puzzle game loop. Modify the UI to include a timer and the "AI agent running..." status.
4.  **Termination Logic**: Enhance the game loop to periodically check for the background process's completion. If completed, the puzzle will announce it and exit automatically.

### Phase 3: Refinements and Packaging
**Goal**: Polish the tool, add comprehensive error handling, and prepare it for easy installation and distribution.

1.  **Robust Input**: Improve the user input handling to support commands like `quit`, `hint`, or `redraw board`.
2.  **Error Handling**: Implement robust error checks for network issues, invalid user input, and other potential failures.
3.  **Packaging**: Configure `pyproject.toml` for proper packaging with `pip`, enabling the creation of a runnable `chess-puzzle-cli` command.