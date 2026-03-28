import gradio as gr
from rag import CoursePlannerRAG

planner = CoursePlannerRAG()

def chat_fn(message, history):
    """
    Standard chat interface function.
    Handles general queries and prerequisite checks.
    """
    response = planner.prereq_check(message)
    return response

def plan_fn(completed, major, term):
    """
    Function specifically for the 'Course Plan' tab.
    """
    courses = [c.strip() for c in completed.split(",") if c.strip()]
    response = planner.generate_plan(courses, major=major, term=term)
    return response

# Custom CSS for glassmorphism look
custom_css = """
footer {visibility: hidden}
.gradio-container {background-color: #f8f9fa}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="MIT Course Advisor") as demo:
    gr.Markdown("# 🎓 MIT Course 6 (EECS) Advisor Assistant (RAG)")
    gr.Markdown("Agentic RAG grounded in official MIT Course Catalog & Policies.")
    
    with gr.Tabs():
        with gr.Tab("💬 Chat & Prereqs"):
            gr.ChatInterface(
                fn=chat_fn,
                examples=[
                    "Can I take 6-1200J if I took 6-01?",
                    "What are the prerequisites for 6-033?",
                    "Do I need instructor consent for 6-08?",
                    "Is 6-036 offered in the Fall 2027 semester?"
                ],
                title="Ask about Prerequisites & Policies"
            )
            
        with gr.Tab("🗓️ Course Planning"):
            with gr.Row():
                with gr.Column():
                    completed_input = gr.Textbox(label="Completed Courses (comma separated)", placeholder="6-01, 18.01, ...")
                    major_input = gr.Dropdown(choices=["6-1", "6-2", "6-3", "6-4"], label="Select Major", value="6-3")
                    term_input = gr.Radio(choices=["Fall", "Spring"], label="Target Term", value="Fall")
                    plan_btn = gr.Button("Generate Suggested Plan", variant="primary")
                with gr.Column():
                    plan_output = gr.Markdown(label="Suggested Course Plan")
            
            plan_btn.click(fn=plan_fn, inputs=[completed_input, major_input, term_input], outputs=plan_output)

    gr.Markdown("---")
    gr.Markdown("### 📜 Features\n- **Grounded reasoning**: Cites specific catalog sections.\n- **Chain reasoning**: Multi-hop prerequisite verification.\n- **Safe abstention**: Refuses to guess policy not in documentation.")

if __name__ == "__main__":
    demo.launch(share=False)

