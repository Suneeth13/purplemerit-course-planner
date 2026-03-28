import gradio as gr
from rag import CoursePlannerRAG

planner = CoursePlannerRAG()

def chat_fn(message, history):
    response = planner.prereq_check(message)
    return response

def plan_fn(completed, major, term):
    courses = [c.strip() for c in completed.split(",") if c.strip()]
    response = planner.generate_plan(courses, major=major, term=term)
    return response

# Premium Glassmorphism & Modern UI CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

body, .gradio-container {
    background: linear-gradient(135deg, #1e1e2f, #2a2a40 40%, #151525);
    color: #ffffff;
    min-height: 100vh;
}

/* Glassmorphism Cards */
.gradio-container .gr-box, .gradio-container .gr-panel, .gradio-container .gr-padded {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease-in-out;
}

/* Hover Micro-animations */
button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(138, 43, 226, 0.4) !important;
}

/* Primary Button Styling */
button.primary {
    background: linear-gradient(90deg, #8A2BE2, #4B0082) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
}

/* Chat Bubbles */
.message.bot p { 
    background: rgba(138, 43, 226, 0.1) !important; 
    border-left: 3px solid #8A2BE2;
}
.message.user p { 
    background: rgba(255, 255, 255, 0.1) !important; 
}

/* Inputs & Dropdowns */
input, textarea, .gr-dropdown-input {
    background: rgba(0, 0, 0, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: white !important;
}

input:focus, textarea:focus {
    border-color: #8A2BE2 !important;
    box-shadow: 0 0 10px rgba(138, 43, 226, 0.5) !important;
}

/* Titles and Text */
h1 {
    background: -webkit-linear-gradient(45deg, #e0aaff, #c77dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px !important;
}
.subtitle {
    text-align: center;
    color: #a0a0b0;
    font-size: 1.1em;
    margin-bottom: 25px !important;
}

footer { visibility: hidden !important; display: none !important; }
"""

theme = gr.themes.Monochrome(
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="transparent",
    block_background_fill="transparent"
)

with gr.Blocks(theme=theme, css=custom_css, title="Purple Merit Planner") as demo:
    gr.Markdown("# ✨ MIT Course 6 AI Advisor")
    gr.Markdown("<p class='subtitle'>Premium Agentic RAG grounded in the official MIT Course Catalog.</p>")
    
    with gr.Tabs():
        with gr.Tab("💬 Ask the Advisor"):
            gr.ChatInterface(
                fn=chat_fn,
                examples=[
                    "What are the prerequisites for 6-033?",
                    "Can I take 6-1200J if I took 6-01?",
                    "Do I need instructor consent for 6-08?",
                    "Is 6-036 offered in the Fall 2027 semester?"
                ],
                title="Prerequisites & Policies",
            )
            
        with gr.Tab("🗓️ Term Planner"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🎓 Student Profile")
                    completed_input = gr.Textbox(label="Completed Courses", placeholder="e.g., 6-01, 18.01")
                    major_input = gr.Dropdown(choices=["6-1", "6-2", "6-3", "6-4"], label="Select Major", value="6-3")
                    term_input = gr.Radio(choices=["Fall", "Spring"], label="Target Term", value="Fall")
                    plan_btn = gr.Button("🚀 Generate Curriculum Plan", variant="primary")
                with gr.Column(scale=2):
                    gr.Markdown("### 📋 Suggested Course Plan")
                    plan_output = gr.Markdown(label="")
            
            plan_btn.click(fn=plan_fn, inputs=[completed_input, major_input, term_input], outputs=plan_output)

    gr.Markdown("---")
    gr.Markdown("<div style='text-align: center; color: #888; font-size: 0.9em;'>Powered by Google Gemini & LangChain LCEL • Purple Merit Assessment</div>")

if __name__ == "__main__":
    demo.launch(share=False)

