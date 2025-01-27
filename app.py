import json
import requests
import streamlit as st
import time

def fetch_linkedin_info(profile_url):
    app_id = "f8c4372d-fc4c-4b62-b811-99e590c5503f/"
    api_key = "ww-1vGLJ3ncYG1Vkpr08ukple3S14jClF1RkEp5eUmYOiTlWWAlHOa9Av"

    # Execute the API request
    r = requests.post(
        f"https://app.wordware.ai/api/released-app/{app_id}/run",
        json={
            "inputs": {"profile_url": profile_url},
            "version": "^1.0"
        },
        headers={"Authorization": f"Bearer {api_key}"},
        stream=True
    )

    # Ensure the request was successful
    if r.status_code != 200:
        return f"Request failed with status code {r.status_code}"

    result = ""
    for line in r.iter_lines():
        if line:
            content = json.loads(line.decode('utf-8'))
            value = content['value']
            if value['type'] == "chunk":
                result += value['value']

    # Simulate a delay to ensure proper info fetching
    time.sleep(10)

    # Extract and return only the numbered points
    final_output = []
    for line in result.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
            final_output.append(line.strip())

    return "\n".join(final_output) if final_output else "No data found."

# Streamlit UI
def main():
    st.title("LinkedIn Info Fetcher")
    st.write("Enter a LinkedIn profile URL to fetch information from the Wordware API.")

    # Input field for the LinkedIn profile URL
    profile_url = st.text_input("LinkedIn Profile URL", "")

    # Button to fetch data
    if st.button("Fetch Information"):
        if profile_url.strip():
            with st.spinner("Fetching data..."):
                response = fetch_linkedin_info(profile_url)
            st.text_area("API Response", response, height=200)
        else:
            st.error("Please enter a valid LinkedIn profile URL.")

if __name__ == "__main__":
    main()
