# Dependencies
import streamlit as st
import requests
import webbrowser
import google.generativeai as genai
import re

# Get the APIs keys
GEMINI_API_KEY = "AIzaSyClHfsmtQgIT7SczQwDfYBW3MDJRfpPmOY"
LAIME_API_KEY = "lmwr_sk_9ZWN0ODAZe_QjxwbXtkTw9xupSiuf9KxeXPdGh0F1IlZUl8F"

# Set the Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Create the model
def enhance_prompt(user_text: str, city: str):
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
    ]

    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash-latest",
      safety_settings=safety_settings,
      generation_config=generation_config,
    )

    chat_session = model.start_chat(
      history=[
      ]
    )

    # Here make the Gemini enhance the prompt of the user so it help to give the client amazing image
    message = f"""
    هل يمكنك أن تكتب لي فقرة صغيرة وتسخدم فيها كلمات من هذه الجملة: "{user_text}ولهذه الدولة{city}"
     أريد ان تكون الفقرة صغيرة ولا أريد منك غير أن تجيبني بالفقرة لا شيء آخر سواها
     وأريد أن تكون الفقرة توصف صورة يمكن توليدها بالذكاء الاصطناعي قم بتقديم الفقرة فقط دون العنوان ودون آخر جملة   
    """
    response = chat_session.send_message(message)
    # Extracting the Arabic text from the response
    arabic_text = response.candidates[0].content.parts[0].text

    # Printing the Arabic text
    print(f"[INFO-4]: Arabic text generated: {arabic_text}")
    return arabic_text

# Generate image by LaimWire
def generate_image(url, text_prompt: str):
    payload = {
        "prompt": text_prompt,
        "aspect_ratio": "1:1"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": f"Bearer {LAIME_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
    data = response.json()
    print("[INFO-1]: Data Returned Successfully")
    image_link = data['data'][0]['asset_url']
    print("[INFO-2]: Link of Image is Ready to Open.")
    webbrowser.open(image_link)
    print("[INFO-3]: Image Generated and Opened Successfully...")

# Insert title into the webpage in the center
st.markdown("""<h1 style='text-align: center;
            '>Welcome to Jorda App</h1>""",
             unsafe_allow_html=True)

# Insert some description into the webpage in the center
st.markdown("""<p style="text-align:center;
            font-size:18px;">
            The place where you can
             visit countries
         by the magic of AI</p>""",
             unsafe_allow_html=True)

st.write("##")
st.write("##")
# Create a list of countries
user_option = st.selectbox("What country would you like to imagine with AI?",
                ("مدينة مميزة في الأردن", "مدينة مميز في اسبانيا", "مدينة مميزة في بريطانيا",
                "مدينة مميزة في السعودية", "مدينة مميزة في أمريكا"),
                )

# Create text area for user prompt
user_prompt = st.text_area(label=" ",
                placeholder="...اكتب وصف المدينة التي تريد زيارتها",
                           label_visibility="visible")  # "Write your country description, so AI can imagine and give you amazing image..."

# Show enhanced prompt and give the user choice to choose if he want to use the enhance prompt or the original one
# Create a radio button to select prompt type
prompt_type = st.radio("Select your choice:", ("The enhanced text prompt by AI", "The original text prompt"))


# Getting the url of the generation API
URL = "https://api.limewire.com/api/image/generation"

if prompt_type == "The enhanced text prompt by AI":
    # Create a button for submitting
    press = st.button(label="Create Image")
    if press:
        generate_image(URL, text_prompt=enhance_prompt(user_prompt, user_option))

if prompt_type == "The original text prompt":
    # Create a button for submitting
    press = st.button(label="Create Image")
    if press:
        generate_image(URL, text_prompt=user_prompt)
