# ==============================================================================
# ماژول ارکستراسیون و مدیریت جریان کار (Workflow Orchestration)
# 
# مفاهیم پایه در این ماژول:
# - گره (Node): هر مرحله یا تابع پردازشی مستقل در سیستم (مثل ایجنت محقق یا مجری ابزار).
#   هر گره وضعیت جاری (State) را دریافت کرده، پردازش می‌کند و وضعیت جدید را برمی‌گرداند.
# - یال (Edge): مسیر و جهت انتقال جریان داده بین گره‌ها.
# - یال شرطی (Conditional Edge): تصمیمی که بر اساس وضعیت فعلی، گره بعدی را انتخاب می‌کند
#   (مثلاً اگر ابزار صدا زده شد برو به گره Tools، در غیر این صورت کار را پایان بده).
# - گراف (Graph): نقشه کلی این گره‌ها و یال‌ها که جریان خودکار و چرخه‌ای کار را مدیریت می‌کند.
# ==============================================================================
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.graph.state import AgentState
from app.agents.researcher import get_research_agent
from app.tools.search import web_search


# تعریف ابزارهای مجاز در گراف
tools = [web_search]
tool_node = ToolNode(tools)

def call_researcher(state: AgentState):
    """گره اجرای ایجنت محقق"""
    agent = get_research_agent()
    response = agent.invoke(state["messages"])
    # خروجی جدید به لیست messages اضافه می‌شود
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """
    یال شرطی: تصمیم‌گیری درباره اینکه آیا باید ابزار صدا زده شود یا کار تمام است.
    """
    last_message = state["messages"][-1]
    # اگر ایجنت درخواست اجرای ابزار داده بود
    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        return "tools"
    return END

def create_research_graph():
    """ساخت و کامپایل کردن گراف اولیه"""
    workflow = StateGraph(AgentState)

    # ۱. اضافه کردن گره‌ها
    workflow.add_node("researcher", call_researcher)
    workflow.add_node("tools", tool_node)

    # ۲. تعیین نقطه شروع
    workflow.set_entry_point("researcher")

    # ۳. اضافه کردن یال شرطی از محقق
    workflow.add_conditional_edges(
        "researcher",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    # ۴. برگشت از ابزار به محقق (ایجنت باید نتیجه ابزار را ببیند)
    workflow.add_edge("tools", "researcher")

    return workflow.compile()