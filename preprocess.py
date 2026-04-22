import pandas as pd
import spacy
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess_reviews(csv_path="realistic_restaurant_reviews.csv"):
    df = pd.read_csv(csv_path)
    
    processed_reviews = []
    
    for idx, row in df.iterrows():
        text = row["Title"] + " " + row["Review"]
        
        # Process with spaCy
        doc = nlp(text)
        
        # Clean text: remove stop words, lemmatize
        cleaned_tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        cleaned_text = " ".join(cleaned_tokens)
        
        # Detect language (simple heuristic)
        lang = "en" if any(token.lang_ == "en" for token in doc) else "unknown"
        
        processed_reviews.append({
            "original_title": row["Title"],
            "original_review": row["Review"],
            "cleaned_text": cleaned_text,
            "rating": row["Rating"],
            "date": row["Date"],
            "language": lang
        })
    
    # Save processed data
    processed_df = pd.DataFrame(processed_reviews)
    processed_df.to_csv("processed_reviews.csv", index=False)
    print("Preprocessing complete. Saved to processed_reviews.csv")

if __name__ == "__main__":
    preprocess_reviews()