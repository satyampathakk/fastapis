from fastapi import FastAPI, Request
import google.generativeai as genai
from scrapper import scrape_patent_data
app = FastAPI()
#genai.configure(api_key="AIzaSyC-MxhBy1IpkwfyUNbLgyPkCFpqAs8_Cig")
# Load generative model
model = genai.GenerativeModel("gemini-pro")

@app.post("/")
async def search_patent(request: Request):
    data = await request.json()  # Extract JSON data from request
    text = data.get("text")
    genai.configure(api_key=data.get("key"))

    # Construct the text with the check text
    check_text = "give me only minimum 5-7 word to so that i can search on google patent to match my idea with any which is relevant remember your response should be those 5-7 word nothing else"

    # Start the generative chat model and send the first message
    chat = model.start_chat()
    res = chat.send_message(text + check_text)

    # Scrape patent data using the model's response
    file_data=scrape_patent_data(res.text)

    # Read additional data from file
    prompt = ("commpare both idea and tell if any thing is common in them i am giving "
              "you abstrat idea of both the project with intentiono of identifying if my idea "
              "is different and can be put to publish and patent tell your opinion if they are "
              "similar and what way before this prompt the idea which is ours is given and after "
              "this text all the idea which are on google patent is there with its patent no . In "
              "response mention the patent number also")

    # Send the second message for comparison
    response = chat.send_message(text + prompt + file_data)

    # Return the response in JSON format
    return {"results": response.text}
