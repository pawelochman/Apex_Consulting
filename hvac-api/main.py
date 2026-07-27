@app.post("/hvac")
def hvac_answer(payload: Question):
    response = _client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Answer this HVAC question: {payload.question}"
    )

    # Defensive checks
    if not response.candidates:
        return {"answer": "Model returned no candidates."}

    parts = response.candidates[0].content.parts
    if not parts:
        return {"answer": "Model returned empty content."}

    # Extract text safely
    answer = "".join([p.text for p in parts if hasattr(p, "text")])

    if not answer:
        return {"answer": "Model returned no text content."}

    return {"answer": answer}
