import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
import json
import nltk

# Ensure NLTK is ready
nltk.download('punkt')

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LangChain Groq model
llm = ChatGroq(model="qwen-2.5-32b")


# Define State for workflow
class State(TypedDict):
    video_url: str
    transcript: str
    blog_title: str
    blog: str
    review: str


# Function to fetch transcript from YouTube video
def get_youtube_transcript(video_url):
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]  # Extract Video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # Fetch transcript
        return "\n".join([entry["text"] for entry in transcript])  # Convert transcript to text
    except Exception as e:
        return f"Error: {str(e)}"


# Step 1: Transcript Generation
def transcript_generation(state: State) -> State:
    state["transcript"] = get_youtube_transcript(state["video_url"])
    return state


# Step 2: Blog Generation
def blog_generation(state: State) -> State:
    response = llm.invoke([
        SystemMessage(content="You are a professional blog writer."),
        HumanMessage(content=f"Generate a well-structured blog post from this YouTube transcript:\n{state['transcript']}")
    ])
    # Split the response into title and content
    response_content = response.content.split("\n", 1)
    state["blog"] = response_content[1] if len(response_content) > 1 else response_content[0]
    state["blog_title"] = response_content[0]  # The first part is the title
    
    return state


# Step 3: Blog Analysis (Pass/Fail)
def analyze_blog_with_AI(state: State):
    prompt = f"""
    Analyze the following blog and provide a single quality score (0-100).
    Higher score means better readability, grammar, and engagement.

    Blog:
    {state['blog']}

    Respond in JSON format:
    {{
        "overall_score": 85
    }}
    """
    
    response = llm.invoke([
        SystemMessage(content="You are an AI that evaluates blog quality."),
        HumanMessage(content=prompt)
    ])
    
    result = json.loads(response.content)
    score = result.get("overall_score", 0)

    return "Pass" if score >= 85 else "Fail"


# Step 4: Blog Improvement if Needed
def improve_blog_quality(state: State) -> State:
    response = llm.invoke([
        SystemMessage(content="You are an expert blog writer. Improve the blog while keeping it engaging."),
        HumanMessage(content=f"Enhance the following blog:\n{state['blog']}")
    ])
    # Split the response into title and content
    response_content = response.content.split("\n", 1)
    state["blog"] = response_content[1] if len(response_content) > 1 else response_content[0]
    state["blog_title"] = response_content[0]  # The first part is the title
    
    return state


# Build the LangGraph workflow
workflow = StateGraph(State)

# Add workflow steps
workflow.add_node("transcriptor", transcript_generation)
workflow.add_node("blogger", blog_generation)
workflow.add_node("reviewer", improve_blog_quality)

# Define conditional edge based on blog score
workflow.add_edge(START, "transcriptor")
workflow.add_edge("transcriptor", "blogger")
workflow.add_conditional_edges("blogger", analyze_blog_with_AI, {"Fail": "reviewer", "Pass": END})
workflow.add_edge("reviewer", END)

# Compile workflow
chain = workflow.compile()

# ──────────────────────────── Streamlit UI ────────────────────────────
st.title("📺 YouTube Blog Generator 📺")
st.write("Convert YouTube videos into well-structured blog posts effortlessly!")

# User input for YouTube link
youtube_link = st.text_input("🎥 Enter YouTube Video Link: 🎥")

# Submit button to trigger blog generation
if st.button("Generate Blog"):
    if youtube_link:
        with st.spinner("Fetching transcript and generating blog..."):
            state = chain.invoke({"video_url": youtube_link})

            if "Error" in state["transcript"]:
                st.error(state["transcript"])
            else:
                # Display Generated Blog
                if "blog_title" in state:  # Ensure the title exists
                    st.subheader(f"📚 {state['blog_title']}")  # Display the catchy title
                else:
                    st.subheader("📝 Generated Blog Title (Fallback)")

                # Display the Blog Content
                blog_lines = state["blog"].split("\n")
                st.write("\n".join(blog_lines))

    else:
        st.warning("⚠️ Please enter a valid YouTube link.")
