"""
Test script for tools in the src/tools directory.
This script tests functionalities of various tools implemented.
"""

import os
from unittest.mock import patch
from src.tools.build_directory_tree import build_directory_tree
from src.tools.delete_file import delete_file
from src.tools.execute_command import execute_command
from src.tools.read_docstring import read_docstring


def test_build_directory_tree():
	"""Test the build_directory_tree function."""
	try:
		result = build_directory_tree()
		print("Directory Tree:\n", result)
	except Exception as e:
		print("Error while building directory tree:", e)


def test_delete_file():
	"""Test the delete_file function."""
	try:
		# Create a temporary file for testing
		test_file = "temp_test_file.txt"
		with open(test_file, "w", encoding="utf-8") as f:
			f.write("Test content")

		result = delete_file(test_file)
		print("Delete File Result:", result)
	except Exception as e:
		print("Error in delete_file:", e)


def test_execute_command():
	"""Test the execute_command function."""
	try:
		# Mock input to simulate approval
		with patch('builtins.input', return_value='yes'):
			command = "echo Hello"
			result = execute_command(command, os.getcwd())
			print("Execute Command Result:", result)
	except Exception as e:
		print("Error in execute_command:", e)


def test_read_docstring():
	"""Test the read_docstring function."""
	try:
		result = read_docstring("src/__init__.py")
		print("Read Docstring Result:", result)
	except Exception as e:
		print("Error in read_docstring:", e)


if __name__ == "__main__":
	test_build_directory_tree()
	test_delete_file()
	test_execute_command()
	test_read_docstring()
