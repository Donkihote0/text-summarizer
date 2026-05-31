# summarizer.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from keybert import KeyBERT
import torch
import streamlit as st

class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn", device=-1):
        """
        device=-1: dùng CPU
        device=0: dùng GPU (nếu có)
        """
        with st.spinner("Đang tải model (lần đầu có thể mất 1-2 phút)..."):
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.device = device
            
            if device >= 0 and torch.cuda.is_available():
                self.model.to(torch.device(f"cuda:{device}"))
                st.success("✅ Đã tải model lên GPU")
            else:
                st.success("✅ Đã tải model (CPU mode)")
        
        self.kw_model = KeyBERT()
    
    def summarize(self, text, max_length=150, min_length=30):
        """
        Tóm tắt văn bản
        """
        # Tokenize
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True
        )
        
        if self.device >= 0 and torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        
        # Generate summary
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        
        # Decode
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    def extract_keywords(self, text, top_n=5):
        """
        Trích xuất từ khóa
        """
        # Cắt text nếu quá dài
        if len(text) > 5000:
            text = text[:5000]
        
        keywords = self.kw_model.extract_keywords(
            text, 
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=top_n
        )
        return [kw[0] for kw in keywords]