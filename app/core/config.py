from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # این متغیرها از فایل .env خوانده می‌شوند
    project_name: str = "AI Research Team"
    version: str = "0.1.0"
    
    # کلید API برای مدل‌های زبانی (بدون دیفالت تا اجباری باشد)
    openai_api_key: str
    
    # آدرس دیتابیس برای ذخیره وضعیت Jobها
    database_url: str = "sqlite:///./jobs.db"

    # تنظیمات Pydantic برای خواندن از فایل .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# ساخت یک نمونه Singleton از کانفیگ برای کل اپلیکیشن
settings = Settings()