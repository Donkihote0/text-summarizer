# Tiện ích
import re
import streamlit as st

def clean_text(text: str) -> str:
    """Làm sạch văn bản: xóa khoảng trắng thừa, ký tự đặc biệt"""
    # Giữ lại dấu câu cơ bản
    text = re.sub(r'\s+', ' ', text)  # Gộp nhiều space/newline
    text = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', '', text)  # Xóa ký tự đặc biệt nhưng giữ . , ! ? - ' "
    return text.strip()

def read_uploaded_file(uploaded_file) -> str:
    """Đọc nội dung file .txt"""
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            try:
                return uploaded_file.read().decode("utf-8")
            except:
                return uploaded_file.read().decode("latin-1")
        else:
            st.error("Hiện chỉ hỗ trợ file .txt")
            return ""
    return ""

def truncate_text(text: str, max_chars: int = 4000) -> str:
    """Cắt văn bản nếu quá dài để tránh lỗi memory"""
    if len(text) > max_chars:
        st.warning(f"⚠️ Văn bản dài {len(text)} ký tự. Hệ thống sẽ chỉ xử lý {max_chars} ký tự đầu tiên.")
        return text[:max_chars]
    return text

def estimate_reading_time(text: str) -> int:
    """Ước tính thời gian đọc (phút)"""
    word_count = len(text.split())
    reading_speed = 200  # từ/phút
    return max(1, round(word_count / reading_speed))