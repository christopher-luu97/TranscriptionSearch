<h1>Welcome to the Transcription Webapp</h1>
This webapp utilizes a frontend of react with typescript, tailwindcss and a backend using Django.
The backend logic for transcription uses the WhisperX package.

You can view a demonstration of the application here:
https://youtu.be/oGWeaHt4V7A

To run this yourself, you must have Docker installed.
Then in cmd type: docker-compose up
Everything takes a while to spin up due to the image size, which I aim to reduce in the future.
The application image works all locally on your desktop, so depending on your input file, it can take a while to process.

Alternatively, you can run this in developer mode:

1. cloning the repo
2. in /frontend, run npm install for all the packages
3. in /backend, run pip install -r requirements.txt after creating the relevant Python virtual environment
4. in the Python virtual environment run pip install git+https://github.com/m-bain/whisperx.git
   - Note: for installation for the whipserX, you can follow https://github.com/m-bain/whisperX
5. Once all packages from npm and pip have finished you can then proceed to spinup the backend and frontend
6. for frontend, navigate to /frontend in the cmd and type: npm run start
7. for backend, navigate to /backend and in the cmd within your python venv type: python manage.py runserver
8. The apps should be exposed on: localhost:3000 for frontend, localhost:8000 for backend api
9. You can view what's going on via cmd for frontend and backend when you started up the servers

Use cases for this application:

- Text analysis for long-form audio
- Generate subtitles automatically for your own videos

TODO:

1. Let user download results to different formats (COMPLETE)
   - TXT, CSV, SRT, VTT
2. Let user input from youtube link
   - Currently only accepts pre-downloaded files
3. Add separate folder to store temporary uploaded files and remove them when done (COMPLETE)
   - Currently stored at same level directory as manage.py in /backend
4. Add search functionality
   - Lexical search (COMPLETE)
   - Semantic search
     - (maybe using vector search methods and embeddings)
   - Reduced search should have two buttons: Download ALL (this downloads all the data) and Download Filtered (Downloads only results of search)
5. Fix search functionality to keep memory of original data. Subsequent searches and clicking reset button only works on filtered data, losing original data.
6. Improved styling and look of the app with SVG and more animations
7. For mp4/youtube uploads, display the video itself, replacing the animated waveform for audio only inputs
