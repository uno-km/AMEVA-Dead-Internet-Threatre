import unittest
from src.core.prompt_adapter import PromptAdapter

class TestPromptAdapter(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.adapter = PromptAdapter()

    async def test_build_structured_history(self):
        """Verify that the structured history avoids script/dialogue layout by using stances"""
        items = [
            {"bot_name": "bot_1", "message": "I disagree."},
            {"bot_name": "bot_2", "message": "Why?"}
        ]
        history = await self.adapter.build_structured_history(items)
        
        self.assertIn("[Conversation History]", history)
        self.assertIn("- bot_1's stance:", history)
        self.assertIn("- bot_2's stance:", history)
        
        # Verify no script colon format is present
        self.assertNotIn("\nbot_1:", history)

    async def test_empty_history(self):
        self.assertEqual(await self.adapter.build_structured_history([]), "No previous conversation.")

if __name__ == '__main__':
    unittest.main()
