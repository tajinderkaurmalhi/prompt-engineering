import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import time
import os
import sys

# 🔑 Set your Gemini 2.0 Flash API key here
GOOGLE_API_KEY = "AIzaSyCinnrFJHds_HUj5IsFx5_8_mp4ksJs8MA"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# 📥 Fetch website content
def fetch_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')
        markdown = md(str(soup.body))
        return text, markdown, soup
    except Exception as e:
        print(f"Error fetching website: {e}")
        return "", "", None

# 🧠 Summarize using Gemini 2.0 Flash
def summarize_with_gemini(text):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": f"Summarize the following webpage content in well-formatted markdown:\n\n{text}"
            }]
        }]
    }

    response = requests.post(f"{GEMINI_URL}?key={GOOGLE_API_KEY}", headers=headers, json=data)
    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        print("Error from Gemini response:", response.json())
        return "Summary could not be generated."

# 💾 Save summary to file
def save_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# 🔄 Reframe summary
def reframe_summary(summary):
    return summary.replace("In summary,", "To wrap things up,").replace("Overall,", "In conclusion,")

# 🔗 Extract internal/external links
def extract_links(soup, base_url):
    internal, external = set(), set()
    domain = base_url.split("//")[-1].split("/")[0]
    if not soup:
        return [], []

    for tag in soup.find_all('a', href=True):
        href = tag['href']
        if href.startswith('/'):
            internal.add(base_url + href)
        elif domain in href:
            internal.add(href)
        elif href.startswith("http"):
            external.add(href)
    return list(internal), list(external)

# 🎞 Typewriter effect - character-by-character
def typewriter(text, delay=0.008, pause_on_punctuation=True):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if pause_on_punctuation and char in ".!?":
            time.sleep(delay)  # Longer pause after sentence
        else:
            time.sleep(delay * 6)
    print("\n")

# 🚀 Main function
def main():
    url = input("🌐 Enter website URL to summarize: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print("\n📡 Fetching website content...")
    text, markdown, soup = fetch_website_content(url)

    print("🤖 Summarizing using Gemini 2.0 Flash...")
    summary = summarize_with_gemini(text)

    os.makedirs("summaries", exist_ok=True)
    original_path = "summaries/original_summary.md"
    reframed_path = "summaries/reframed_summary.md"

    save_to_file(summary, original_path)

    reframed = reframe_summary(summary)
    save_to_file(reframed, reframed_path)

    internal_links, external_links = extract_links(soup, url)

    print("\n📝 Original Summary:\n")
    typewriter(summary)

    print("\n📝 Reframed Summary:\n")
    typewriter(reframed)

    print("\n🔗 Internal Links Found:")
    for link in internal_links:
        print(" -", link)

    print("\n🌍 External Links Found:")
    for link in external_links:
        print(" -", link)

if _name_ == "_main_":
    main()
