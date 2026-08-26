#!/usr/bin/env python3
"""
Project 1: Rule-Based AI Chatbot  --  "THE LOGIC ENGINE"
Artificial Intelligence | Industrial Training Kit | DecodeLabs (Batch 2026)

GOAL
    Create a simple rule-based chatbot that responds to predefined user inputs.

THE BLUEPRINT: IPO MODEL
    INPUT    (Raw Feed)          ->  Sanitization & Normalization
    PROCESS  (Logic Skeleton)    ->  Intent Matching  (O(1) hash-map lookup)
    OUTPUT   (Feedback Loop)     ->  Response Generation

PROJECT 1 SPECIFICATION: THE LOGIC SKELETON
    [x] INPUT LOOP     : continuous 'while' cycle
    [x] SANITIZATION   : handle case & whitespace
    [x] KNOWLEDGE BASE : dictionary with 5+ intents
    [x] FALLBACK       : default response for unknowns
    [x] EXIT STRATEGY  : clean break command

DESIGN NOTE
    The if-elif ladder is the anti-pattern: linear complexity O(n) and high
    technical debt. The knowledge base is therefore a dictionary (hash map)
    resolved with .get() -- lookup and fallback in a single atomic operation,
    in constant time O(1). Explicit if-else logic governs control flow:
    the empty-input guard, the exit command, and the response branch.
"""

import sys

# Emit the box-drawing characters reliably even when stdout is redirected.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):  # pragma: no cover - very old interpreters
    pass


# ---------------------------------------------------------------------------
# PRESENTATION LAYER  --  blueprint palette (cyan / green / orange on dark)
# ---------------------------------------------------------------------------

class Palette:
    """ANSI styles, blanked out automatically when the terminal cannot show them."""

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    ORANGE = "\033[38;5;208m"
    WHITE = "\033[97m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def disable(cls) -> None:
        for name in ("CYAN", "GREEN", "ORANGE", "WHITE", "DIM", "BOLD", "RESET"):
            setattr(cls, name, "")


def enable_colour() -> None:
    """Turn on ANSI rendering, or strip it if the stream is not a real console."""
    if not sys.stdout.isatty():
        Palette.disable()
        return
    if sys.platform == "win32":
        # Ask the Windows console host for virtual-terminal processing.
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            Palette.disable()


WIDTH = 66


def rule(left: str, fill: str, right: str) -> str:
    return f"{Palette.CYAN}{left}{fill * (WIDTH - 2)}{right}{Palette.RESET}"


def framed(text: str, style: str = "") -> str:
    """Centre `text` inside the banner frame, ignoring style codes when padding."""
    pad = WIDTH - 2 - len(text)
    lead, trail = pad // 2, pad - pad // 2
    return (
        f"{Palette.CYAN}│{Palette.RESET}{' ' * lead}{style}{text}"
        f"{Palette.RESET}{' ' * trail}{Palette.CYAN}│{Palette.RESET}"
    )


def show_banner() -> None:
    print()
    print(rule("┌", "─", "┐"))
    print(framed("THE LOGIC ENGINE", Palette.BOLD + Palette.WHITE))
    print(framed("Project 1  ·  Rule-Based AI Chatbot", Palette.CYAN))
    print(framed("DecodeLabs  ·  Batch 2026", Palette.DIM))
    print(rule("└", "─", "┘"))
    print(
        f"  {Palette.DIM}Type {Palette.RESET}{Palette.GREEN}help{Palette.RESET}"
        f"{Palette.DIM} to see what I understand, or "
        f"{Palette.RESET}{Palette.ORANGE}exit{Palette.RESET}"
        f"{Palette.DIM} to end the session.{Palette.RESET}"
    )
    print()


def respond(message: str) -> None:
    """OUTPUT phase: render one bot turn."""
    print(f"  {Palette.CYAN}Bot{Palette.RESET} │ {message}")
    print()


# ---------------------------------------------------------------------------
# KNOWLEDGE BASE  --  seven intents, each with its own trigger set
# ---------------------------------------------------------------------------

INTENTS = {
    "greeting": {
        "triggers": ("hello", "hi", "hey", "good morning", "good evening"),
        "response": "Hello! I am the Logic Engine, a rule-based assistant. "
                    "How can I help you today?",
    },
    "wellbeing": {
        "triggers": ("how are you", "how are you doing", "how's it going"),
        "response": "Running deterministically -- every reply is traced from "
                    "input, through logic, to output.",
    },
    "identity": {
        "triggers": ("who are you", "what is your name", "your name"),
        "response": "I am the Logic Engine, Project 1 of the DecodeLabs AI "
                    "track. I answer from explicit rules, never from guesswork.",
    },
    "capability": {
        "triggers": ("help", "what can you do", "commands", "options"),
        "response": "I recognise greetings, and questions about how I am, who I "
                    "am, what rule-based AI means, and thanks. Say 'exit' to leave.",
    },
    "concept": {
        "triggers": ("what is rule-based ai", "what is ai", "explain rule-based ai"),
        "response": "Rule-based AI is a white box: input maps to output through "
                    "hard-coded rules, so there is zero hallucination risk.",
    },
    "gratitude": {
        "triggers": ("thanks", "thank you", "appreciate it"),
        "response": "You are welcome. Rule matched, response delivered.",
    },
    "farewell": {
        "triggers": ("exit", "quit", "bye", "goodbye", "see you"),
        "response": "Goodbye! The loop is closing cleanly. Keep building.",
    },
}

# THE PIVOT: flatten every trigger into one hash map so each turn is a single
# O(1) direct access instead of an O(n) sequential scan down an if-elif ladder.
KNOWLEDGE_BASE = {
    trigger: intent["response"]
    for intent in INTENTS.values()
    for trigger in intent["triggers"]
}

# EXIT STRATEGY: the kill commands that break the loop.
EXIT_COMMANDS = frozenset(INTENTS["farewell"]["triggers"])

# FALLBACK: the single default served for anything outside the knowledge base.
FALLBACK_RESPONSE = (
    "I do not understand that yet -- it is not in my rule set. "
    "Type 'help' to see what I recognise."
)

EMPTY_INPUT_RESPONSE = "I did not catch anything there. Please type a message."


# ---------------------------------------------------------------------------
# THE HEARTBEAT  --  the infinite loop
# ---------------------------------------------------------------------------

def main() -> None:
    enable_colour()
    show_banner()

    while True:  # INPUT LOOP: the organism stays alive until the kill command.
        try:
            raw_input_text = input(f"  {Palette.GREEN}You{Palette.RESET} │ ")
        except (EOFError, KeyboardInterrupt):
            # Stream closed or Ctrl+C: still leave through the clean exit path.
            print()
            respond(INTENTS["farewell"]["response"])
            break

        # PHASE 1 -- SANITIZATION: fold case and trim surrounding whitespace.
        clean_input = raw_input_text.lower().strip()
        print()

        # PHASE 2 -- PROCESS: explicit if-else control flow over the hash map.
        if not clean_input:
            respond(EMPTY_INPUT_RESPONSE)
        elif clean_input in EXIT_COMMANDS:
            respond(KNOWLEDGE_BASE[clean_input])
            break  # KILL COMMAND: clean break out of the cycle.
        else:
            # Atomic operation: lookup + fallback in one constant-time call.
            reply = KNOWLEDGE_BASE.get(clean_input, FALLBACK_RESPONSE)
            respond(reply)

    print(rule("└", "─", "┘"))
    print(f"  {Palette.DIM}Session ended · The Logic Engine{Palette.RESET}")
    print()


if __name__ == "__main__":
    main()
