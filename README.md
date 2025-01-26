# SambaMedica Project Prototype

## Project Description

SambaMedica idea is to automate the process of generating medical scan image reports (such as X-rays, ultrasounds, or MRIs) using the power of Agentic AI on the SambaNova AI platform. 

The automation begins immediately after a scan is performed, for example, when an X-ray is taken in the hospital laboratory. The image is sent to our system for analysis, which produces a comprehensive report that includes diagnosis, recommendations, and potential next steps or treatments. This analysis considers not only the image but also the patient's medical history and symptoms (this will be future work). The system then automatically forwards the report to the laboratory physician for review and any necessary edits. Once confirmed, the report is saved as a PDF for the patient or the referring doctor to access.

Our technical architecture involves encoding the image as base64 text and simultaneously processing it with two SambaNova vision models (Llama-3.2-11B-Vision-Instruct and Llama-3.2-90B-Vision-Instruct) to extract insights. The results from both models are then combined and sent to the SambaNova text model (Meta-Llama-3.3-70B-Instruct) to generate the final report, including the diagnosis and recommendations.

The implementation of parallel threading with the vision models is crucial in reducing response time. Additionally, combining the outputs of the two SambaNova vision models enhances the overall quality of the report.

The system has been tested using various images related to different diseases, such as breast cancer and chest inflammation, as well as images showing no disease. The results from these tests have been promising, demonstrating the system's effectiveness.

## Setup steps

1.  Setup Environment

    1.  Install Python 3.9.13 or Python 3.10

    2.  Install Python libraries

        1.  pip install flask_cors

        2.  pip install flask

        3.  pip install pillow

        4.  pip install openai

2.  start the application

    1.  Open Terminal

    2.  Change directory to application folder

    3.  Run the following command "Python app.py" this will start the
        Flask server with the application.

3.  Access the application

    1.  access the application in the browser at <http://127.0.0.1:5000>
        (the URL will be taken from the step 2.3 result)
