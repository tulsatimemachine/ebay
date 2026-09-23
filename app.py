import streamlit as st
import base64, json
from openai import OpenAI

st.set_page_config(page_title="eBay SEO Tool", page_icon="🏷️", layout="centered")

st.title("🏷️ eBay SEO Listing Tool")

api_key = st.text_input("OpenAI API Key", type="password")

# Mobile camera capture & file upload widgets
img_source = st.radio("Select Input Source:", ["Camera", "Photo Library"])

if img_source == "Camera":
    img_file = st.camera_input("Take a product photo")
else:
    img_file = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])

if img_file and api_key:
    client = OpenAI(api_key=api_key)
    base64_img = base64.b64encode(img_file.getvalue()).decode("utf-8")
    
    if st.button("Generate Listing", type="primary"):
        with st.spinner("Analyzing photo with GPT-4o..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "Analyze image and return JSON: 'title' (max 80 chars), 'category_id', 'average_price', 'item_specifics', 'description'."},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Generate eBay listing."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]}
                ]
            )
            result = json.loads(response.choices[0].message.content)
            
            st.subheader("eBay Title (Tap to copy)")
            st.code(result.get("title", ""))
            
            st.subheader("Pricing & Category")
            col1, col2 = st.columns(2)
            col1.metric("Est. Price", f"${result.get('average_price', 'N/A')}")
            col2.metric("Category ID", result.get("category_id", "N/A"))
            
            st.subheader("Full Details")
            st.json(result)
