import os
import pytest

# قبل از اینکه هر ماژولی ایمپورت شود، متغیر محیطی ست می‌شود
os.environ["OPENAI_API_KEY"] = "mock_key_for_tests"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"