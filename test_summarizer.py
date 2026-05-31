# test_summarizer.py
from summarizer import TextSummarizer

# Khởi tạo
print("Loading model...")
summarizer = TextSummarizer()
print("Model loaded!")

# Văn bản mẫu ngắn hơn để test nhanh
text = """
Artificial intelligence (AI) is intelligence demonstrated by machines. 
Leading AI textbooks define the field as the study of "intelligent agents". 
AI research includes computer vision, natural language processing, and robotics.
"""

# Tóm tắt
print("\n📝 Summarizing...")
summary = summarizer.summarize(text, max_length=30, min_length=10)
print("Summary:", summary)

# Trích xuất từ khóa
print("\n🏷️ Extracting keywords...")
keywords = summarizer.extract_keywords(text)
print("Keywords:", keywords)