import pytest
from unittest.mock import patch
from langchain_core.messages import AIMessage
from app.agents.researcher import get_research_agent

# با دکوراتور patch، متد invoke را مسدود و با یک شیء قلابی (Mock) جایگزین می‌کنیم
@patch("app.agents.researcher.ChatOpenAI.invoke")
def test_research_agent_calls_tool_mocked(mock_invoke):
    # ۱. ساخت پاسخ شبیه‌سازی‌شده (Mock Response)
    # دقیقاً ساختاری را می‌سازیم که اگر OpenAI ابزار را انتخاب می‌کرد، برمی‌گرداند
    mock_response = AIMessage(
        content="",
        tool_calls=[{
            "name": "web_search", 
            "args": {"query": "LangGraph vs AutoGen"}, 
            "id": "call_mock_123"
        }]
    )
    # به پایتون می‌گوییم هر وقت متد invoke صدا زده شد، این پاسخ ساختگی را برگردان
    mock_invoke.return_value = mock_response

    # ۲. اجرای منطق اصلی برنامه
    agent = get_research_agent()
    response = agent.invoke([
        ("system", "You are a research assistant."),
        ("user", "What are the core differences between LangGraph and AutoGen?")
    ])
    
    # ۳. بررسی نتایج (Assertions)
    assert hasattr(response, "tool_calls"), "Response should contain tool_calls"
    assert len(response.tool_calls) > 0, "Model decided not to use any tool!"
    
    called_tool_name = response.tool_calls[0]["name"]
    assert called_tool_name == "web_search", f"Expected web_search, got {called_tool_name}"
    
    # بررسی نهایی: آیا متد ما واقعاً در جریان تست صدا زده شد؟
    mock_invoke.assert_called_once()