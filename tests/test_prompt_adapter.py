import unittest
from src.core.prompt_adapter import PromptAdapter

class TestPromptAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = PromptAdapter()

    def test_build_structured_history(self):
        """대본 형식 방지 포맷 정상 반환 검증"""
        items = [
            {"bot_name": "bot_1", "message": "I disagree."},
            {"bot_name": "bot_2", "message": "Why?"}
        ]
        history = self.adapter.build_structured_history(items)
        
        self.assertIn("[Conversation History]", history)
        self.assertIn("- speaker=bot_1 | message=\"I disagree.\"", history)
        self.assertIn("- speaker=bot_2 | message=\"Why?\"", history)
        
        # 'bot_1:' 처럼 콜론이 바로 붙는 텍스트가 없는지 확인
        self.assertNotIn("\nbot_1:", history)

    def test_build_structured_history_escaping(self):
        """따옴표/줄바꿈/인젝션 방지 이스케이프 검증"""
        items = [
            {"bot_name": "bot_1", "message": 'I say "hello"\nworld'}
        ]
        history = self.adapter.build_structured_history(items)
        self.assertIn('- speaker=bot_1 | message="I say \\"hello\\" world"', history)

    def test_empty_history(self):
        self.assertEqual(self.adapter.build_structured_history([]), "No previous conversation.")

if __name__ == '__main__':
    unittest.main()
