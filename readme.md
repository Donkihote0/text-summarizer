# AI Text Summarizer
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
## Giới thiệu
**AI Text Summarizer** là ứng dụng thông minh giúp tóm tắt văn bản dài và trích xuất từ khóa tự động, sử dụng các mô hình NLP tiên tiến.

## Tính năng nổi bật
- **Tóm tắt nhanh** văn bản dài (báo, email, bài nghiên cứu)
- **Trích xuất từ khóa** quan trọng
- **Upload file** .txt
- **Tùy chỉnh** độ dài tóm tắt
- **Tải kết quả** dạng file
- **Giao diện web** thân thiện

## Công nghệ sử dụng

| Thành phần | Công nghệ | Mô hình |
|------------|-----------|---------|
| Tóm tắt văn bản | Transformers | BART (Facebook) |
| Trích xuất từ khóa | KeyBERT | Sentence-BERT |
| Giao diện | Streamlit | - |
| Deploy | Hugging Face Spaces | - |

## Cài đặt và chạy local

```bash
# Clone repository
git clone https://github.com/Donkihote0/text-summarizer.git
cd text-summarizer

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```
## Live Demo

**Link:**: [https://text-summarizer-2stns7wrnrsyzssxcl5rzt.streamlit.app/]
