from app.gemini import model

response = model.generate_content("Hello Gemini, confirm connection.")
print(response.text)
