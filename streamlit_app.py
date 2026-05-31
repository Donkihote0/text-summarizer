# app.py
import streamlit as st
from summarizer import TextSummarizer
from utils import clean_text, read_uploaded_file, truncate_text, estimate_reading_time

# Cấu hình trang
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# Tiêu đề
st.title("📝 Trợ lý tóm tắt văn bản thông minh")
st.markdown("*Tóm tắt văn bản dài và trích xuất từ khóa chỉ trong vài giây!*")

# Khởi tạo model (cache lại để không load lại mỗi lần)
@st.cache_resource
def load_model():
    return TextSummarizer()

# Load model
try:
    summarizer = load_model()
except Exception as e:
    st.error(f"❌ Lỗi khi tải model: {e}")
    st.stop()

# Sidebar: Tùy chọn
with st.sidebar:
    st.header("⚙️ Cài đặt")
    max_length = st.slider("Độ dài tóm tắt (từ)", 30, 300, 150, 
                           help="Số từ tối đa trong bản tóm tắt")
    min_length = st.slider("Độ dài tối thiểu (từ)", 20, 100, 30,
                           help="Số từ tối thiểu trong bản tóm tắt")
    num_keywords = st.slider("Số lượng từ khóa", 3, 10, 5)
    
    st.markdown("---")
    st.markdown("### 📌 Hướng dẫn")
    st.markdown("""
    1. **Nhập văn bản** hoặc **upload file**
    2. Điều chỉnh độ dài tóm tắt (nếu cần)
    3. Click **'Tóm tắt ngay!'**
    4. Xem kết quả và tải về
    """)
    
    st.markdown("---")
    st.markdown("### 🧠 Công nghệ")
    st.markdown("""
    - **Tóm tắt:** BART
    - **Từ khóa:** KeyBERT
    - **Giao diện:** Streamlit
    """)

# Main area: Input
col1, col2 = st.columns([2, 1])

with col1:
    input_method = st.radio("Chọn cách nhập văn bản", ["📝 Nhập trực tiếp", "📁 Upload file"], horizontal=True)
    
    text_input = ""
    if input_method == "📝 Nhập trực tiếp":
        text_input = st.text_area(
            "Nhập văn bản của bạn:", 
            height=300,
            placeholder="Ví dụ: Dán một đoạn tin tức, bài báo, email dài vào đây..."
        )
    else:
        uploaded_file = st.file_uploader("Chọn file .txt", type=['txt'])
        if uploaded_file:
            text_input = read_uploaded_file(uploaded_file)
            if text_input:
                st.text_area("Nội dung file:", text_input, height=200, disabled=True)

with col2:
    st.markdown("### 📊 Thông tin văn bản")
    if text_input and text_input.strip():
        char_count = len(text_input)
        word_count = len(text_input.split())
        reading_time = estimate_reading_time(text_input)
        
        st.metric("Số ký tự", f"{char_count:,}")
        st.metric("Số từ", f"{word_count:,}")
        st.metric("Thời gian đọc", f"~{reading_time} phút")
        
        if char_count > 4000:
            st.warning("⚠️ Văn bản dài >4000 ký tự, sẽ tự động cắt bớt")
    else:
        st.info("👈 Nhập hoặc upload văn bản để xem thông tin")

# Button xử lý
col_button, col_empty = st.columns([1, 3])
with col_button:
    process_button = st.button("🚀 Tóm tắt ngay!", type="primary", use_container_width=True)

if process_button:
    if not text_input or not text_input.strip():
        st.error("❌ Vui lòng nhập văn bản hoặc upload file trước!")
    else:
        with st.spinner("🔄 Đang xử lý... (có thể mất 10-30 giây tùy độ dài văn bản)"):
            # Clean và truncate
            clean = clean_text(text_input)
            clean = truncate_text(clean, 4000)
            
            # Tóm tắt
            summary = summarizer.summarize(
                clean, 
                max_length=max_length, 
                min_length=min_length
            )
            
            # Trích xuất từ khóa
            keywords = summarizer.extract_keywords(clean, top_n=num_keywords)
        
        # Hiển thị kết quả
        st.success("✅ Tóm tắt hoàn thành!")
        
        # Tạo 2 cột cho kết quả
        col_out1, col_out2 = st.columns(2)
        
        with col_out1:
            st.subheader("📄 Bản tóm tắt")
            st.markdown(f"> {summary}")
            
            # Nút copy
            st.code(summary, language='text', line_numbers=False)
            
        with col_out2:
            st.subheader("🏷️ Từ khóa chính")
            for i, kw in enumerate(keywords, 1):
                st.markdown(f"{i}. **{kw}**")
        
        # Xuất file
        result_text = f"""TÓM TẮT VĂN BẢN
{'='*50}

📝 BẢN TÓM TẮT:
{summary}

🏷️ TỪ KHÓA CHÍNH:
{', '.join(keywords)}

{'='*50}
Thông tin:
- Số từ gốc: {len(text_input.split()):,}
- Số từ tóm tắt: {len(summary.split()):,}
- Tỷ lệ nén: {len(summary.split())/len(text_input.split())*100:.1f}%
"""
        
        st.download_button(
            label="📥 Tải xuống kết quả (file .txt)",
            data=result_text,
            file_name="summary_result.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Powered by BART and KeyBERT | Made by Donkihote0</div>",
    unsafe_allow_html=True
)
