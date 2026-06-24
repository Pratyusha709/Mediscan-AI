from google import genai
import time

# 🔑 Add your API key here
client = genai.Client(api_key="AIzaSyCmBd9A3iKZQI2q1R4hbgq17Ggw08wV7U8")

def get_chatbot_response(user_input):

    try:
        # 🔥 Try main fast model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        return response.text

    except Exception as e:

        print("⚠️ First model failed, retrying...")

        time.sleep(2)

        try:
            # 🔁 Fallback model (more stable)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=user_input
            )
            return response.text

        except Exception as e2:
            return "Server busy right now 😅 please try again in a few seconds."