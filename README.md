# cimsolutions_emotional_chatbot
Cimsolutions afstudeeropdracht, emotie detectie plugin maken voor chatbots

### Proof of concept
This repo shows a small proof of concept of a chatbot working together with a retrieval based output system.
The retrieval based system uses the dutch robbert language model to detect an emotion in the user input and returns
an answer from a preset of sentences. This answer is combined with the chatbot answer to return a more empathic answer.

### How to run
There are two ways to run this project.

#### Main.py
The first way is running main.py. Note that the first run will take a while due to all the models loading in.

#### Endproduct notebook
There is a endproduct notebook in the notebooks folder. This notebook can be openend using jupyter notebook or google collab.
The notebook contains all the seperate products with small explainations. Note that it was made with google collab in google drive.
In order to make the project work you need to change the variables **path** and **db_path** to the correct path for your file structure.

**Possibly** Git lfs is needed to clone the project due to the model size. Use git lfs clone instead. [git lfs docs](https://git-lfs.com/)
