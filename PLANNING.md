# Chess Puzzle AI CLI Wrapper

## Project Objective

To create an interactive Command Line Interface (CLI) tool that launches a chess puzzle for the user to play while an AI agent (or any other long-running command) executes in the background. The puzzle will feature a timer and an announcement that the AI agent is running. Users can continue playing the puzzle until the AI agent completes its task or they choose to exit the puzzle.

## High-Level Vision & Architecture

The `chess-puzzle-ai-cli` will function as an interactive companion CLI tool, designed to be launched by an external AI agent (e.g., Gemini CLI, Claude Code). Its primary purpose is to provide an engaging chess puzzle experience to the user while the AI agent performs long-running background tasks.

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

## Workflow

1.  **AI Agent Invocation**: An external AI agent (e.g., Gemini CLI) initiates a long-running task and, in parallel, invokes `chess-puzzle-ai-cli` as a sub-process. The AI agent passes necessary communication parameters (e.g., a path to a shared clock file, a task completion signal file) to `chess-puzzle-ai-cli`.
    *   *Example Invocation*: `gemini run chess-puzzle-ai-cli --clock-file /tmp/gemini_clock.txt --status-file /tmp/gemini_status.txt`
2.  **Communication Setup**: `chess-puzzle-ai-cli` establishes a communication channel with the invoking AI agent to receive real-time updates on the AI agent's task progress (e.g., a ticking clock) and eventual task completion.
3.  **Interactive Puzzle Launch**: Upon successful communication setup, `chess-puzzle-ai-cli` launches its interactive chess puzzle UI in the foreground.
    *   The UI will display:
        *   A chessboard.
        *   A counting clock, synchronized with the AI agent's progress.
        *   A user input area for making moves.
        *   A dedicated area for displaying feedback, including incorrect or illegal moves.
        *   A dynamic menu bar at the bottom, offering commands such as "Terminate Puzzle" (to return control to the AI agent) and displaying notifications like "AI Task Completed!".
4.  **Continuous Monitoring & Interaction**: The chess puzzle loop continuously:
    *   Updates the displayed clock based on signals from the AI agent.
    *   Processes user chess moves, validates them, and updates the board.
    *   Monitors the AI agent's task completion status.
5.  **Termination Conditions**:
    *   **AI Task Completion**: When the AI agent signals task completion, the puzzle UI will notify the user and offer options to either continue playing the puzzle or return to the AI agent's prompt.
    *   **User Termination**: The user can explicitly terminate the puzzle via the menu bar, returning control to the AI agent.
6.  **Graceful Exit**: Upon any termination condition, `chess-puzzle-ai-cli` will gracefully exit, ensuring the terminal is restored to its original state and any communication channels are properly closed.

## Phased Implementation Plan

We will adopt a block-by-block development approach, ensuring a functional component at the end of each phase.

### Phase 1: Core Puzzle UI with External Communication Hooks
**Goal**: Develop a fully functional, interactive chess puzzle CLI tool, capable of displaying a board, handling basic user input, and establishing initial communication with an external source for clock synchronization and task status.

1.  **Project Setup**: Initialize a Python project with `pyproject.toml` to manage dependencies (`python-chess`, `requests`, `berserk`, `prompt-toolkit`).
2.  **Display Default Board & Pieces**: Adapt and integrate the board and piece display logic from `cli-chess` to render a colorized chessboard and pieces in the terminal using `prompt-toolkit` with a default starting position.
3.  **Initial External Communication & Clock Display**:
    *   Implement command-line arguments (`--clock-file`, `--status-file`) to receive paths for communication.
    *   Implement a basic file-reading mechanism to periodically read a simulated clock value from `--clock-file`.
    *   Adapt the existing `cli-chess` clock module to read from the designated clock file instead of an internal timer. This will involve a `ClockModel` that reads the file and a `ClockPresenter` that updates the `ClockView`.
    *   Display this external clock value in the UI.
4.  **Basic User Input & Feedback**:
    *   Implement a user input area for chess moves.
    *   Add a new UI component (e.g., another `TextArea` or `FormattedTextControl`) to display messages about incorrect moves or illegal moves.
5.  **Interactive Game Loop (Basic)**: Adapt the core game loop to incorporate the external clock display and basic user input.

### Phase 2: AI Agent Communication & Enhanced UI
**Goal**: Establish robust communication with an external AI agent and enhance the UI to reflect the AI agent's status and provide comprehensive user interaction.

1.  **Refined Communication Protocol & Termination Signaling**:
    *   Implement a more robust file-based protocol (or named pipes, if deemed necessary after initial testing) for real-time clock synchronization and task completion signals.
    *   Implement a mechanism to signal back to the AI agent if the puzzle is terminated by the user.
2.  **Dynamic UI Elements & Notifications**:
    *   Implement the dynamic menu bar with a "Terminate Puzzle" option.
    *   Implement the "AI Task Completed!" notification display using a dedicated `AlertContainer`.
3.  **Process Monitoring (Passive)**: Implement logic to passively monitor the AI agent's process status (e.g., checking if the PID passed via argument is still active) to handle unexpected AI agent termination.
4.  **Puzzle Integration**: Integrate fetching and displaying actual chess puzzles from the Lichess API.

### Phase 3: Robustness, Packaging, and Advanced Features
**Goal**: Polish the tool, add comprehensive error handling, and prepare it for easy installation and distribution, along with any advanced features.

1.  **Comprehensive Error Handling**: Implement robust error checks for network issues, invalid user input, and other potential failures.
2.  **Packaging**: Configure `pyproject.toml` for proper packaging with `pip`, enabling the creation of a runnable `chess-puzzle-cli` command.
3.  **Advanced Puzzle Features**: Implement features such as a hint system and puzzle difficulty selection.
4.  **Configuration for Communication**: Allow users to configure communication parameters (e.g., file paths, polling intervals) via a configuration file.