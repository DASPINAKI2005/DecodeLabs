#!/usr/bin/env python3
"""
Project 2: Data Classification Using AI  --  THE PROXIMITY ENGINE
Artificial Intelligence | Industrial Training Kit | DecodeLabs (Batch 2026)

GOAL
    Train a K-Nearest Neighbors classifier on the Iris dataset.
    Load data, split into train/test, fit KNN, evaluate accuracy and
    deeper metrics (confusion matrix, classification report).

THE BLUEPRINT: SUPERVISED LEARNING PIPELINE
    INPUT    (Raw Dataset)         ->  Load & Explore
    PROCESS  (Proximity Engine)     ->  Train KNN Model
    OUTPUT   (Validation)          ->  Accuracy + Classification Report

PROJECT 2 SPECIFICATION: THE PROXIMITY ENGINE
    [x] LOAD DATA       : Iris benchmark (150 samples, 3 classes, 4 features)
    [x] UNDERSTAND DATA  : shape, class distribution, feature statistics
    [x] SPLIT DATA       : 80/20 train-test split with stratification
    [x] CLASSIFY         : K-Nearest Neighbors (K=5)
    [x] VALIDATE         : accuracy, confusion matrix, classification report

DESIGN NOTE
    KNN is the simplest supervised algorithm: it stores every training
    point and classifies a new sample by majority vote of its K nearest
    neighbours. No rules are written -- the machine derives decision
    boundaries purely from the data.
"""

import sys
import os

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
)


# ---------------------------------------------------------------------------
# PRESENTATION LAYER  --  blueprint palette
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
    if not sys.stdout.isatty():
        Palette.disable()
        return
    if sys.platform == "win32":
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
    pad = WIDTH - 2 - len(text)
    lead, trail = pad // 2, pad - pad // 2
    return (
        f"{Palette.CYAN}│{Palette.RESET}{' ' * lead}{style}{text}"
        f"{Palette.RESET}{' ' * trail}{Palette.CYAN}│{Palette.RESET}"
    )


def show_banner() -> None:
    print()
    print(rule("┌", "─", "┐"))
    print(framed("THE PROXIMITY ENGINE", Palette.BOLD + Palette.WHITE))
    print(framed("Project 2  ·  KNN Classification", Palette.CYAN))
    print(framed("DecodeLabs  ·  Batch 2026", Palette.DIM))
    print(rule("└", "─", "┘"))
    print()


def section(title: str) -> None:
    print(f"\n  {Palette.BOLD}{Palette.ORANGE}── {title} ──{Palette.RESET}\n")


def info(label: str, value: str) -> None:
    print(f"  {Palette.CYAN}{label:20s}{Palette.RESET} {value}")


def success(msg: str) -> None:
    print(f"  {Palette.GREEN}✔ {msg}{Palette.RESET}")


# ---------------------------------------------------------------------------
# PHASE 1: LOAD & UNDERSTAND  --  raw material inspection
# ---------------------------------------------------------------------------

def load_and_explore():
    """Load the Iris dataset and print structural information."""
    section("PHASE 1: LOAD & UNDERSTAND")

    iris = load_iris()
    X, y = iris.data, iris.target
    names = iris.target_names

    info("Dataset", "Iris (sklearn)")
    info("Samples", str(X.shape[0]))
    info("Features", str(X.shape[1]))
    info("Classes", ", ".join(names))
    print()

    for i, name in enumerate(names):
        count = int(np.sum(y == i))
        print(f"    {Palette.GREEN}●{Palette.RESET} {name:12s}  {count} samples")

    print()
    info("Feature names", ", ".join(iris.feature_names))
    info("Data range", f"{X.min():.1f} — {X.max():.1f} cm")

    return X, y, names


# ---------------------------------------------------------------------------
# PHASE 2: SPLIT & SCALE  --  train/test partitioning
# ---------------------------------------------------------------------------

def split_and_scale(X, y):
    """Split into train/test and standardize features."""
    section("PHASE 2: SPLIT & SCALE")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    info("Split ratio", "80% train / 20% test")
    info("Train set", f"{X_train.shape[0]} samples")
    info("Test set", f"{X_test.shape[0]} samples")

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    info("Scaling", "StandardScaler (z-score)")
    success("Data ready for classification")

    return X_train_s, X_test_s, y_train, y_test


# ---------------------------------------------------------------------------
# PHASE 3: CLASSIFY  --  K-Nearest Neighbors
# ---------------------------------------------------------------------------

def classify(X_train, y_train, X_test, k=5):
    """Fit KNN and predict on the test set."""
    section("PHASE 3: CLASSIFY (KNN)")

    info("Algorithm", "K-Nearest Neighbors")
    info("K value", str(k))
    info("Distance metric", "Euclidean")
    print()

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    success("Model trained and predictions generated")

    return y_pred


# ---------------------------------------------------------------------------
# PHASE 4: VALIDATE  --  accuracy is not enough
# ---------------------------------------------------------------------------

def validate(y_test, y_pred, class_names):
    """Evaluate predictions with accuracy, confusion matrix, and report."""
    section("PHASE 4: OUTPUT VALIDATION")

    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"  {Palette.BOLD}Accuracy: {Palette.GREEN}{acc:.4f} ({acc*100:.1f}%){Palette.RESET}")
    print()

    # The accuracy mirage: warn when data might be imbalanced.
    print(f"  {Palette.DIM}Note: Accuracy alone can be misleading on imbalanced data.{Palette.RESET}")
    print(f"  {Palette.DIM}We also inspect the confusion matrix and per-class metrics.{Palette.RESET}")
    print()

    # Confusion matrix
    print(f"  {Palette.BOLD}Confusion Matrix:{Palette.RESET}")
    header = "  " + " " * 12 + "  ".join(f"{Palette.CYAN}{c:>10s}{Palette.RESET}" for c in class_names)
    print(header)
    for i, row in enumerate(cm):
        label = f"{Palette.GREEN}{class_names[i]:>10s}{Palette.RESET}"
        cells = "  ".join(f"{v:10d}" for v in row)
        print(f"  {label}  {cells}")
    print()

    # Classification report
    print(f"  {Palette.BOLD}Classification Report:{Palette.RESET}")
    report = classification_report(y_test, y_pred, target_names=class_names, digits=4)
    for line in report.splitlines():
        print(f"    {line}")
    print()

    if acc >= 0.95:
        success(f"Model is highly accurate ({acc*100:.1f}%)")
    elif acc >= 0.80:
        success(f"Model performs well ({acc*100:.1f}%)")
    else:
        print(f"  {Palette.ORANGE}⚠ Accuracy is below 80%. Consider tuning K or features.{Palette.RESET}")

    return acc


# ---------------------------------------------------------------------------
# THE HEARTBEAT
# ---------------------------------------------------------------------------

def main():
    enable_colour()
    show_banner()

    X, y, class_names = load_and_explore()
    X_train, X_test, y_train, y_test = split_and_scale(X, y)
    y_pred = classify(X_train, y_train, X_test)
    acc = validate(y_test, y_pred, class_names)

    print(rule("└", "─", "┘"))
    print(f"  {Palette.DIM}Project 2 complete · The Proximity Engine{Palette.RESET}")
    print(f"  {Palette.DIM}Accuracy: {acc*100:.1f}% · KNN on Iris{Palette.RESET}")
    print()


if __name__ == "__main__":
    main()
