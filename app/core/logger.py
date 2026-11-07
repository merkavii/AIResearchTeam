import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    پیکربندی لاگر استاندارد برای کل پروژه.
    در محیط Production این لاگ‌ها می‌توانند به Datadog یا ELK ارسال شوند.
    """
    logger = logging.getLogger(name)
    
    # اگر از قبل هندلر داشت، دوباره اضافه نمی‌کنیم تا لاگ‌ها تکراری چاپ نشوند
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # فرمت استاندارد شامل زمان، نام ماژول و پیام
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # لاگ‌ها را در خروجی استاندارد ترمینال (stdout) چاپ می‌کنیم
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

# یک نمونه لاگر سراسری برای دسترسی سریع
logger = setup_logger("research_team")