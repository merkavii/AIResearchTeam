from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    وضعیت مرکزی گراف. تمام گره‌ها این دیکشنری را به عنوان ورودی دریافت
    کرده و تغییرات را به صورت دیکشنری برمی‌گردانند.
    """
    # لیست پیام‌ها با قانون الحاق (Append-only) از طریق add_messages مدیریت می‌شود
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # شمارنده تلاش‌های مجدد برای جلوگیری از لوپ بی‌نهایت
    retry_count: int