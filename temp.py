import json
import requests
import gradio as gr

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

    # Extract and return only the numbered points
    final_output = []
    for line in result.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
            final_output.append(line.strip())
    
    return "\n".join(final_output) if final_output else "No data found."

# Create the Gradio interface
interface = gr.Interface(
    fn=fetch_linkedin_info,
    inputs=gr.Textbox(label="LinkedIn Profile URL"),
    outputs=gr.Textbox(label="API Response", interactive=False),
    title="LinkedIn Info Fetcher",
    description="Enter a LinkedIn profile URL to fetch information from the Wordware API."
)

# Launch the app
interface.launch()
