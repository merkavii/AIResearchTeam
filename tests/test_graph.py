from unittest.mock import patch
from langchain_core.messages import HumanMessage, AIMessage
from app.graph.workflow import create_research_graph

@patch("app.agents.researcher.ChatOpenAI.invoke")
def test_research_graph_execution(mock_invoke):
    # مرحله اول: مدل تصمیم می‌گیرد ابزار web_search را فراخوانی کند
    first_response = AIMessage(
        content="",
        tool_calls=[{
            "name": "web_search",
            "args": {"query": "LangGraph state management"},
            "id": "call_graph_001"
        }]
    )
    # مرحله دوم: بعد از دریافت نتیجه ابزار، پاسخ نهایی متنی را تولید می‌کند
    final_response = AIMessage(content="LangGraph uses a centralized state machine.")
    
    mock_invoke.side_effect = [first_response, final_response]

    app = create_research_graph()

    initial_input = {
        "messages": [HumanMessage(content="Explain LangGraph state management.")],
        "retry_count": 0
    }

    # اجرای گراف تا رسیدن به گره پایانی
    result = app.invoke(initial_input)

    # بررسی صحت اجرای مراحل در گراف
    assert "messages" in result
    # پیام‌ها باید شامل: سوال کاربر -> فراخوانی ابزار -> خروجی ابزار -> پاسخ نهایی باشد
    assert len(result["messages"]) >= 4
    assert result["messages"][-1].content == "LangGraph uses a centralized state machine."