from langchain_core.tools import tool
from app.core.logger import logger

@tool
def web_search(query: str) -> str:
    """
    Searches the web for up-to-date information based on the user's query.
    Always use this tool when you need facts, news, or external references.
    """
    logger.info(f"Tool executed: web_search | Query: '{query}'")
    
    try:
        # در اینجا کد واقعی اتصال به اینترنت قرار می‌گیرد
        # برای شبیه‌سازی یک خطای شبکه‌ای، اگر کوئری کلمه 'error' را داشت Exception می‌دهیم
        if "error" in query.lower():
            raise ConnectionError("Simulated network timeout during search.")
            
        mock_results = f"Mock Results for '{query}': LangGraph is a framework for stateful apps."
        logger.info("Tool finished successfully.")
        return mock_results
        
    except Exception as e:
        # ! به جای توقف برنامه، ارور را به مدل برمی‌گردانیم تا خودش هندل کند
        error_msg = f"Search failed due to an error: {str(e)}. Please try a different query or proceed with existing knowledge."
        logger.error(error_msg)
        return error_msg