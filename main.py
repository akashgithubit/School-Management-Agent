import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# ✅ Initialize AI model
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="ibm-granite/granite-4.0-h-micro",  # or "anthropic/claude-3.5-sonnet"
    max_tokens=2048
)

UPLOAD_DIR = "uploads"

def get_latest_uploaded_file():
    """Return the most recently uploaded Excel/CSV file."""
    files = [os.path.join(UPLOAD_DIR, f) for f in os.listdir(UPLOAD_DIR)]
    if not files:
        print("⚠️ No uploaded files found. Please upload one via the API first.")
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file


def load_school_data(file_path: str):
    """Read uploaded Excel/CSV file into a DataFrame."""
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path, encoding="latin1", on_bad_lines="skip")
    else:
        df = pd.read_excel(file_path)
    return df


if __name__ == "__main__":
    print("🔍 Checking for uploaded school data...")

    file_path = get_latest_uploaded_file()
    if not file_path:
        exit()

    print(f"📂 Using uploaded file: {file_path}\n")

    df = load_school_data(file_path)
    print("📘 School Data Loaded Successfully!\n")
    print(df.head())

    # Create summaries
    class_summary = (
        df.groupby("Class")[["Maths", "Science", "English", "Social", "Total Marks"]]
        .mean()
        .round(2)
    )
    attendance_summary = df.groupby("Class")["Attendance %"].mean().round(2)

    print("\n📊 Average Marks per Class:")
    print(class_summary)
    print("\n📅 Average Attendance per Class:")
    print(attendance_summary)

    # Interactive Q&A
    while True:
        q = input("\nAsk your School AI Agent (type 'exit' to quit): ")
        if q.lower() == "exit":
            print("👋 Exiting School Management AI Agent. Goodbye!")
            break

        data_summary = {
            "Full Student Records": df.to_dict(orient="records"),
            "Classwise Average Marks": class_summary.to_dict(),
            "Classwise Attendance": attendance_summary.to_dict(),
        }

        prompt = (
            "You are a helpful school performance assistant. "
            "Use the data to answer accurately. "
            f"Data: {data_summary}\n"
            f"Question: {q}"
        )

        try:
            response = llm.invoke(prompt)
            print("\n🤖 AI Response:")
            print(response.content, "\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")

