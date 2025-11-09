import os
import streamlit as st
from PIL import Image
import io
import base64
import openai # Import the OpenAI library

# ---- Configuration ----
st.set_page_config(page_title="AI Food Scanner 🍽️", layout="centered", page_icon="🍲")

# ---- OpenAI API Key Configuration ----
# Load from Streamlit secrets or environment variable
# Set your key in `.streamlit/secrets.toml` as OPENAI_API_KEY or set the
# environment variable OPENAI_API_KEY. Do NOT commit your real key.
openai_api_key = None
if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key or not openai_api_key.startswith("sk-"):
    st.warning("OPENAI_API_KEY not found or invalid. Set it in .streamlit/secrets.toml or as environment variable.")
    st.stop()

try:
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=openai_api_key)
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}. Please check your API key.")
    st.stop()

# Function to encode image to base64
def encode_image_to_base64(image_bytes, image_format):
    """Encodes image bytes to a base64 string suitable for OpenAI Vision API."""
    buffered = io.BytesIO()
    # Ensure correct format for encoding (e.g., JPEG or PNG)
    # Re-open the image from bytes to ensure it's a valid PIL Image before saving
    img_for_save = Image.open(io.BytesIO(image_bytes))
    if image_format == "image/jpeg":
        img_for_save.save(buffered, format="JPEG")
    elif image_format == "image/png":
        img_for_save.save(buffered, format="PNG")
    else:
        raise ValueError("Unsupported image format. Please upload JPG or PNG.")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# ---- Title ----
st.title("🍽️ AI Food Image Scanner (powered by OpenAI)")
st.write("Upload a food image to get nutritional insights, calories, and diet suggestions using OpenAI's GPT-4o.")

# ---- Image Uploader ----
food_image = st.file_uploader("📸 Upload a food image", type=["jpg", "jpeg", "png"])

# ---- Analyze Image ----
if food_image:
    # Read the image bytes from the uploaded file
    image_bytes = food_image.read()
    image = Image.open(io.BytesIO(image_bytes)) # PIL Image object for display

    st.image(image, caption="Uploaded Food Image", use_column_width=True)

    try:
        base64_image = encode_image_to_base64(image_bytes, food_image.type)
    except ValueError as e:
        st.error(str(e))
        st.stop()


    # Define the prompt for OpenAI's GPT-4o
    prompt = (
        "You are a certified food and nutrition expert. Analyze the food shown in this image and provide the following:\n"
        "- Food item name (if recognized)\n"
        "- Approximate calories (provide a range if unsure)\n"
        "- Macronutrients (Proteins, Carbs, Fats) in grams or percentage\n"
        "- Health benefits\n"
        "- Suitability for various diets (e.g., Keto, Vegan, Vegetarian, Diabetic, Gluten-Free, Low-Carb)\n"
        "- Pros and cons of consuming this food item\n"
        "Please provide the information in a clear, well-structured, and easy-to-read format, using bullet points or headings where appropriate."
    )

    st.info("Analyzing image using OpenAI's GPT-4o... Please wait. This may take a few moments.")

    try:
        # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o", # Recommended for multimodal capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{food_image.type};base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000, # Limit the response length
        )

        # Display the response
        st.subheader("🍽️ Nutritional Analysis:")
        if response.choices and response.choices[0].message.content:
            st.markdown(response.choices[0].message.content)
        else:
            st.warning("No analysis text received from the AI. The image might be unclear or the model had an issue.")

    except openai.APIConnectionError as e:
        # Handle connection errors (e.g., network issues, DNS problems)
        st.error(f"OpenAI API Connection Error: Could not connect to the OpenAI API. Please check your internet connection or proxy settings. Details: {e}")
        st.warning("This usually means your app can't reach OpenAI's servers.")
    except openai.APIStatusError as e:
        # Handle API errors with a status code (e.g., 400, 401, 429, 500)
        st.error(f"OpenAI API Error: Status {e.status_code} - {e.response.json().get('error', {}).get('message', 'No message available')}")
        st.warning("Please check your API key, subscription status, or try again later. You might have exceeded your quota.")
    except Exception as e:
        # Catch any other unexpected errors
        st.error(f"An unexpected error occurred during AI analysis: {e}")
        st.warning("Please try uploading a different image or check your internet connection.")

# --- How to run this app ---
st.sidebar.markdown("### How to Run This App:")
st.sidebar.markdown("1. Save the code as `app.py`.")
st.sidebar.markdown("2. Make sure you have `streamlit`, `openai`, and `Pillow` installed: \n `pip install streamlit openai Pillow`")
st.sidebar.markdown("3. Your OpenAI API key is already included in the code. **For production use, strongly consider using Streamlit Secrets.**")
st.sidebar.markdown("4. Run from your terminal in the directory where you saved the file: \n `streamlit run app.py`")