import streamlit as st
import json
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini eBay SEO Tool", page_icon="🏷️")
st.title("🏷️ eBay SEO Tool (Powered by Gemini)")

api_key = st.text_input("Gemini API Key", type="password")
img_source = st.radio("Select Input Source:", ["Camera", "Photo Library"])

if img_source == "Camera":
    uploaded_file = st.camera_input("Take a product photo")
else:
    uploaded_file = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    client = genai.Client(api_key=api_key)
    image = Image.open(uploaded_file)
    
    if st.button("Generate Listing", type="primary"):
        with st.spinner("Gemini is analyzing the image..."):
            
            system_prompt = """
            Analyze the image and return JSON:
            1. "title": Cassini eBay title (max 80 chars).
            2. "category_id": Estimated category ID integer.
            3. "average_price": Estimated market price float.
            4. "item_specifics": Key attributes object.
            5. "description": Feature bullets.
            """
            
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.2
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[image, "Generate eBay listing details."],
                config=config
            )
            
            result = json.loads(response.text)
            
            st.subheader("eBay Title (Tap code block to copy)")
            st.code(result.get("title", ""))
            
            col1, col2 = st.columns(2)
            col1.metric("Est. Market Price", f"${result.get('average_price', 'N/A')}")
            col2.metric("Category ID", result.get("category_id", "N/A"))
            
            st.subheader("All Listing Details")
            st.json(result)
