# PDFGPT

This is a plugin developed for GPT-4. 

DEMO:
![image](https://github.com/aryan619348/PDFGPT/assets/46323314/849a063d-d4c4-4d58-845b-3c67b21fd807)

Can also be accesed at http://localhost:5000/ :
<img width="1677" alt="image" src="https://github.com/aryan619348/PDFGPT/assets/46323314/548ebece-56e0-4cbd-810a-b9e27fc2b024">


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
