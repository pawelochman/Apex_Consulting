@app.post("/hvac")
def hvac_answer(payload: Question):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Answer this HVAC question: {payload.question}"
    )

    # Extract Gemini text correctly
    answer = response.candidates[0].content.parts[0].text
    return {"answer": answer}
