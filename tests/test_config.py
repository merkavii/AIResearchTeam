import os
from app.core.config import Settings

def test_settings_load_successfully(monkeypatch):
    # تنظیم مقادیر محیطی موقت برای محیط ایزوله تست
    monkeypatch.setenv("OPENAI_API_KEY", "test_mock_key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    
    # بررسی اینکه Pydantic مقادیر را به درستی می‌خواند
    settings = Settings()
    assert settings.openai_api_key == "test_mock_key"
    assert settings.database_url == "sqlite:///./test.db"