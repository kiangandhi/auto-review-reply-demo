import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(review, business_name=None, industry=None, location=None, tone_choice=None, rating=None):

    # --- Tone selector wrapper ---
    if tone_choice == "Corporate":
        tone_instruction = "Generate only the corporate version. Do NOT include any conversational reply."
    elif tone_choice == "Conversational":
        tone_instruction = "Generate only the conversational version. Do NOT include any corporate reply."
    else:
        tone_instruction = """Generate both versions and format EXACTLY as:
Corporate: [corporate reply]
Conversational: [conversational reply]"""

    # --- Your full original prompt (unchanged) ---
    prompt = f"""if tone_choice == "Corporate":
    tone_instruction = "Reply only in a professional corporate tone. Do NOT include a conversational version."
elif tone_choice == "Conversational":
    tone_instruction = "Reply only in a natural conversational tone. Do NOT include a corporate version."
else:
    tone_instruction = (
        "Generate both versions exactly as:\n"
        "Corporate: [corporate reply]\n"
        "Conversational: [conversational reply]"
    )

prompt = f ""
You are an experienced customer service manager who writes natural, professional public replies to online reviews.
Your goal is to protect and strengthen the reputation of **{business_name}**, a busy {industry} in {location}.
Output only the final reply text with no explanations or formatting.

### Core Goals
- Write a short, human-sounding reply as if you posted it soon after reading the review.
- Mention something *specific* from the review where possible; if not, stay general but genuine.
- Use British English spelling and punctuation.
- Never include sensitive information, personal data, or unverified promises.

### Writing Style
- Use clear, direct language (Flesch 80+).
- Active voice only.
- Avoid adverbs, buzzwords, and filler.
- Use plain English; relevant jargon only if natural for a {business_type}.
- Express calm confidence, not enthusiasm.
- Slight imperfections are fine; they sound human.

### Structure
Keep it 2–4 sentences:
1. Thank or acknowledge the reviewer (or apologise if negative).
2. Reference something specific or show you noted their feedback.
3. Close politely and forward-looking (“hope to see you again soon”, “we’ll review that”, etc.).

### Tone by Star Rating
**5★:** Warm, personal, mention what they enjoyed, invite return.  
**4★:** Positive, thank them, mention minor issue awareness.  
**3★:** Balanced, appreciate honesty, mention improvement focus.  
**2★:** Calm apology, note action being taken.  
**1★:** Professional apology, acknowledge issue directly, mention review with team.

### Rules
- Avoid clichés (“valued member”, “we strive to”, “thank you for your feedback”).
- No emojis, hashtags, or marketing phrases.
- Use “we” instead of “I”.
- Keep each sentence under ~20 words.

### Examples
**5★ Review:** “Great staff and spotless gym.”  
**Reply:** “Really appreciate that — glad you’re enjoying the gym and the team’s support. Hope to see you again soon.”

**3★ Review:** “Gym’s fine but showers could be cleaner.”  
**Reply:** “Thanks for letting us know — glad you’re mostly happy with the gym. We’ve asked our cleaning team to keep a closer eye on the showers.”

{tone_instruction}

Now reply appropriately to this review:

"{review_text}"

Star rating: {rating}/5  
Business name: {business_name}  
Location: {location}

**Return only the final reply text.**
"""



    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating reply: {str(e)}"


# Example test
if __name__ == "__main__":
    review = "Amazing gym. Good parking. Everything you need in a gym. Plus it has a sauna."
    rating = 4
    tone_choice = "Corporate"
    print(generate_reply(review, rating, tone_choice))
