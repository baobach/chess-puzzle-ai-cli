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

## Folder Structure

The `src/chess_puzzle_ai_cli/` directory is organized into the following subdirectories:

*   **`core/`**: This directory contains the core functionalities of the application. It houses the main logic that orchestrates the interaction between various modules and drives the overall program flow when CLI commands are executed. Functions here are responsible for gluing together the different components to run the program.

*   **`modules/`**: This directory is dedicated to modular features and components. Each subdirectory within `modules/` represents a distinct feature or set of related functionalities, such as:
    *   Displaying the chess board.
    *   Handling chess piece representation and movement.
    *   Implementing legal move validation.
    *   Loading and managing chess puzzles.
    *   Any other additional features that can be developed and maintained independently.

*   **`tests/`**: This directory is for organizing all unit and integration tests. It mirrors the structure of `core/` and `modules/` to ensure that tests are co-located with the code they validate, facilitating better development practices and easier debugging.

*   **`utils/`**: This directory contains utility functions and helper scripts that are used across different parts of the application. These are general-purpose functions that support the main program logic but do not belong to a specific core or module feature.

## Proposed Technology Stack

**Language**: Python 3

**Key Libraries:**

*   [python-chess](https://github.com/niklasf/python-chess): For handling all chess-related logic, board states, and move validation. (>=1.9.4,<2.0.0)
*   [requests](https://github.com/psf/requests): For making HTTP requests to fetch chess puzzles from an external API. (^2.28.1)
*   [berserk](https://github.com/lichess-org/berserk): A Lichess API client for Python. (>=0.13.1,<0.14.0)
*   [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit): For building interactive command-line applications. (==3.0.47)
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