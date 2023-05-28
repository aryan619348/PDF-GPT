# PDF-GPT

The goal for this project was to develop a plugin for OpenAI and a Website for PDF-GPT.

Website is at https://pdfgptaryan.azurewebsites.net/
<img width="1680" alt="Screenshot 2023-05-28 at 4 22 08 PM" src="https://github.com/aryan619348/PDF-GPT/assets/46323314/9e276237-f64b-47ef-860d-23fbc533c131">

The plugin can also be accesed at the same link https://pdfgptaryan.azurewebsites.net/
In the plugin store, select the "Install an unverified plugin" option and then use the link.

DEMO for the plugin:
<img width="1417" alt="Screenshot 2023-05-28 at 10 41 33 PM" src="https://github.com/aryan619348/PDF-GPT/assets/46323314/412f138d-c82c-4b14-83b3-99925a61d791">


Can also be accesed locally at http://localhost:80/ :


In order to use this repository:

1. Clone the repository.
2. Install all the neccesary libraries using the pip install -r /path/to/requirements.txt
3. Set the two neccesary API keys in the application.py file:
   1. OPEN_API_KEY (https://platform.openai.com/account/api-keys)
   2. Google Drive Api Key (https://console.cloud.google.com/getting-started)
4. After setting up the API keys from the console run python application.py
5. This should start the server at localhost:5000
6. You can now access the web-interface at http://localhost:5000/ to test the API
7. Go to https://chat.openai.com/?model=gpt-4-plugins
8. From the list of plugins select the "Plugin store" option 
9. Then Select "Develop your own Plugin"
10. The enter the Domain, which is "localhost:5000" in our case:
<img width="739" alt="image" src="https://github.com/aryan619348/PDFGPT/assets/46323314/b5b515cd-ac29-458a-b291-b9703d77e1d6">

10. Click "Find Manifest File" and you should be good to go!
11. In the prompt enter the google drive link to your pdf and start asking away 😃 
