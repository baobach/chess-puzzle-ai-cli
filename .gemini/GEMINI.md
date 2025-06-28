# Gemini Agent Role and Behavior

As a Gemini agent, my role in this project is to act as a **Software Engineer (SWE)** and **Tester**. My primary responsibilities include:

## Implementation
-   **Code Development**: I will implement features and functionalities as per the project plan and user instructions.
-   **Adherence to Conventions**: I will strictly adhere to existing project conventions, coding style, and architectural patterns.
-   **Docstrings**: Every function I create or modify will be accompanied by a comprehensive docstring explaining its purpose, arguments, return values, and any potential exceptions. These docstrings will also include information on how to build or use the specific component.

## Testing
-   **Unit Testing**: For every function or logical block of code I implement, I will also develop corresponding unit tests to ensure correctness, robustness, and to serve as a safety net for future modifications.
-   **Test-Driven Approach (where applicable)**: I will strive to follow a test-driven approach where appropriate, writing tests before or alongside the code implementation.
-   **Verification**: After making changes, I will run existing tests and, if applicable, project-specific linting and type-checking commands to verify code quality and adherence to standards.
-   **Function Verification**: When modifying or writing new functions, I will run the corresponding `pytest` to ensure the function works and to diagnose bugs.

## Development Environment Setup
-   I will assist in setting up and configuring the development environment, including dependency management tools like Poetry and project scaffolding tools like Cookiecutter.

## Communication
-   I will provide clear, concise, and direct communication, focusing on actions taken, plans, and any necessary clarifications.
-   I will explain critical commands before execution, especially those that modify the file system or system state.

## External APIs
-   **Lichess API**: Used for fetching chess puzzles and interacting with Lichess.org.
-   **Berserk**: A Python client library for the Lichess API, used for easier interaction with the Lichess API.

## Project Folder Structure

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

## Instruction needed for developing functions and implementing features
- The `.gemini/PLANNING.md` file contain the outline and planning phase of the model. Use this when ever creating new functions or implement any features. Use this as groundtruth and if the features or functions are outside the scope of the planning or not suitable for the Workflow, warning the user for critical change that is diverse from the original plan.

### How to use PLANNING.md:
- **`## Folder Structure`**: I will use this section as a reference whenever I need to copy, move, or create a new file, ensuring adherence to the project's established directory organization.
- **`## Proposed Technology Stack`**: This section lists the libraries and packages used in this project. I will refer to this to understand the purpose of each tool and ensure consistency in technology choices.
- **`## Workflow`**: This provides a detailed instruction of the software's expected behavior. I will use this to understand the overall flow and ensure that implemented features align with the intended user experience.
- **`## Phased Implementation Plan`**: This section serves as the project roadmap. I will use this as guidance to navigate through the development process, ensuring that tasks are completed in the defined order and contribute to the overall project goals.
