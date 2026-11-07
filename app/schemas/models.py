from pydantic import BaseModel, Field
from datetime import datetime

class ResearchRequest(BaseModel):
    """مدل داده ورودی کاربر یا n8n"""
    # محدودیت طولی می‌گذاریم تا از درخواست‌های بی‌معنی جلوگیری شود
    query: str = Field(..., min_length=10, description="موضوع اصلی تحقیق")
    max_retries: int = Field(default=3, description="حداکثر دفعات تلاش مجدد Reviewer")
    
class JobResponse(BaseModel):
    """مدل پاسخ اولیه پس از ثبت درخواست در سیستم"""
    job_id: str = Field(..., description="شناسه یکتای درخواست")
    status: str = Field(..., description="وضعیت فعلی (مثلاً PENDING)")
    message: str = Field(..., description="پیام وضعیت برای کاربر")
    created_at: datetime = Field(default_factory=datetime.utcnow)