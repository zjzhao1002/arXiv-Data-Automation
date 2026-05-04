import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from arxivflow.ollama_functions import OllamaFunctions

class TestOllamaModelChecker(unittest.TestCase):
    
    @patch('ollama.list')
    def test_exact_match(self, mock_list):
        # Setup mock
        mock_list.return_value = MagicMock(models=[{'model': 'llama3.2:latest'}, {'model': 'gemma:2b'}])
        
        # Test exact match
        obj = OllamaFunctions('llama3.2:latest')
        self.assertTrue(obj._ollama_model_checker())
        self.assertEqual(obj.model_name, 'llama3.2:latest')

    @patch('ollama.list')
    def test_base_name_match_latest(self, mock_list):
        # Setup mock
        mock_list.return_value = MagicMock(models=[{'model': 'llama3.2:latest'}])
        
        # Test base name matching :latest
        obj = OllamaFunctions('llama3.2')
        self.assertTrue(obj._ollama_model_checker())
        self.assertEqual(obj.model_name, 'llama3.2:latest')

    @patch('ollama.list')
    def test_base_name_match_tag(self, mock_list):
        # Setup mock
        mock_list.return_value = MagicMock(models=[{'model': 'llama3.2:3b'}])
        
        # Test base name matching a specific tag
        obj = OllamaFunctions('llama3.2')
        self.assertTrue(obj._ollama_model_checker())
        self.assertEqual(obj.model_name, 'llama3.2:3b')

    @patch('ollama.list')
    def test_no_match(self, mock_list):
        # Setup mock
        mock_list.return_value = MagicMock(models=[{'model': 'gemma:2b'}])
        
        # Test no match
        obj = OllamaFunctions('llama3.2')
        self.assertFalse(obj._ollama_model_checker())
        self.assertEqual(obj.model_name, 'llama3.2')

    @patch('ollama.list')
    @patch('ollama.pull')
    def test_init_pulls_if_not_found(self, mock_pull, mock_list):
        # Setup mock
        mock_list.return_value = MagicMock(models=[{'model': 'gemma:2b'}])
        
        # This will call _ollama_model_checker and then _ollama_pull_model
        obj = OllamaFunctions('llama3.2')
        mock_pull.assert_called_with('llama3.2')

    @patch('ollama.list')
    @patch('ollama.pull')
    def test_init_no_pull_if_found(self, mock_pull, mock_list):
        # Setup mock
        mock_list.return_value = MagicMock(models=[{'model': 'llama3.2:3b'}])
        
        # This will call _ollama_model_checker which returns True
        obj = OllamaFunctions('llama3.2')
        mock_pull.assert_not_called()
        self.assertEqual(obj.model_name, 'llama3.2:3b')

if __name__ == '__main__':
    unittest.main()
