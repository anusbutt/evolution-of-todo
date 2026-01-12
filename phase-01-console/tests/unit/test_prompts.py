"""Unit tests for Prompts module.

This module tests user input collection and validation functionality.
"""

import sys
from io import StringIO
from unittest.mock import patch
import pytest

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.cli.prompts import get_menu_choice


def test_get_menu_choice_valid_input():
    """Test get_menu_choice accepts valid input (1-7)."""
    for valid_choice in ['1', '2', '3', '4', '5', '6', '7']:
        with patch('builtins.input', return_value=valid_choice):
            choice = get_menu_choice()
            assert choice == int(valid_choice)


def test_get_menu_choice_invalid_numeric():
    """Test get_menu_choice rejects out-of-range numbers."""
    # Input: 9 (invalid) returns None
    with patch('builtins.input', return_value='9'):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            choice = get_menu_choice()

        assert choice is None
        output = captured_output.getvalue()
        assert "Invalid choice" in output
        assert "1 and 7" in output


def test_get_menu_choice_negative_number():
    """Test get_menu_choice rejects negative numbers."""
    # Input: -5 (invalid) returns None
    with patch('builtins.input', return_value='-5'):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            choice = get_menu_choice()

        assert choice is None
        output = captured_output.getvalue()
        assert "Invalid choice" in output


def test_get_menu_choice_zero():
    """Test get_menu_choice rejects zero."""
    # Input: 0 (invalid) returns None
    with patch('builtins.input', return_value='0'):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            choice = get_menu_choice()

        assert choice is None
        output = captured_output.getvalue()
        assert "Invalid choice" in output


def test_get_menu_choice_non_numeric():
    """Test get_menu_choice rejects non-numeric input."""
    # Input: "abc" (invalid) returns None
    with patch('builtins.input', return_value='abc'):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            choice = get_menu_choice()

        assert choice is None
        output = captured_output.getvalue()
        assert "Please enter a number" in output


def test_get_menu_choice_empty_input():
    """Test get_menu_choice rejects empty input."""
    # Input: "" (invalid) returns None
    with patch('builtins.input', return_value=''):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            choice = get_menu_choice()

        assert choice is None
        output = captured_output.getvalue()
        assert "Please enter a number" in output


def test_get_menu_choice_whitespace_input():
    """Test get_menu_choice rejects whitespace-only input."""
    # Input: "   " (invalid) returns None
    with patch('builtins.input', return_value='   '):
        captured_output = StringIO()
        with patch('sys.stdout', captured_output):
            choice = get_menu_choice()

        assert choice is None
        output = captured_output.getvalue()
        assert "Please enter a number" in output


def test_get_menu_choice_returns_none_on_first_invalid():
    """Test get_menu_choice returns None on first invalid input (doesn't loop)."""
    # Single invalid input should return None without looping
    with patch('builtins.input', return_value='abc'):
        choice = get_menu_choice()
        assert choice is None


def test_get_menu_choice_strips_whitespace():
    """Test get_menu_choice strips leading/trailing whitespace."""
    # Input with whitespace should be accepted
    with patch('builtins.input', return_value='  3  '):
        choice = get_menu_choice()
        assert choice == 3
