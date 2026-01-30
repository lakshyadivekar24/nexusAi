import os
from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

app = Flask(__name__)

def enhance_prompt(user_input):
    try:
        meta_prompt = f"""
        You are an Expert Prompt Engineer capable of writing prompts for LLMs (ChatGPT) and Diffusion Models (Midjourney/Runway).
        
        USER'S INPUT: "{user_input}"
        
        INSTRUCTIONS:
        1. **Analyze the Request:** Determine if the user wants Text/Code generation OR Image/Video generation.
        
        ---
        
        ### IF IT IS A TEXT/CODE REQUEST:
        Rewrite it using the 'CO-STAR' framework.
        Structure:
        ### ROLE
        [Persona]
        ### TASK
        [What to do]
        ### CONTEXT
        [Details]
        ### STYLE
        [Tone/Voice]
        
        ---
        
        ### IF IT IS AN IMAGE/VIDEO REQUEST:
        Rewrite it as a highly detailed visual prompt.
        Focus on: Subject, Art Style, Lighting, Camera Angle, Color Palette, and Parameters.
        Structure:
        ### 🎨 VISUAL PROMPT
        [Insert the detailed prompt here, e.g., "A futuristic cyberpunk city, neon rain, cinematic lighting, shot on Sony A7R IV, 8k resolution..."]
        
        ### ⚙️ PARAMETERS
        [Suggest settings like: --ar 16:9 (Aspect Ratio), --v 6.0 (Version), or --style raw]
        
        ### 💡 NEGATIVE PROMPT (What to avoid)
        [e.g., "Blurry, low quality, distorted hands, watermark"]
        
        ---
        
        **CRITICAL:** Only output the format relevant to the user's request. Do not output both.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=meta_prompt
        )
        
        return response.text
    except Exception as e:
        return f"Error: {str(e)}. Check API Key."

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_prompt = ""
    user_input = ""
    
    if request.method == 'POST':
        user_input = request.form.get('raw_idea')
        if user_input:
            generated_prompt = enhance_prompt(user_input)
    
    return render_template('index.html', prompt=generated_prompt, original=user_input)

if __name__ == '__main__':
    app.run(debug=True)