from flask import Flask, request, jsonify, send_file

from flask_cors import CORS

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from reportlab.lib.styles import getSampleStyleSheet


import pickle

import os


from dotenv import load_dotenv


from groq import Groq


from resume_parser import extract_text





app = Flask(__name__)


CORS(app)





# Load environment variables

load_dotenv()






# Groq API


client = Groq(

    api_key=os.getenv("GROQ_API_KEY")

)








# Load ML model


model = pickle.load(

    open("../model.pkl","rb")

)




vectorizer = pickle.load(

    open("../vectorizer.pkl","rb")

)








skills_list = [


    "python",

    "java",

    "javascript",

    "sql",

    "html",

    "css",

    "machine learning",

    "react",

    "flask",

    "mongodb",

    "c++",

    "data science",

    "ai",

    "django"


]









@app.route("/check", methods=["POST"])


def check_resume():



    file = request.files["resume"]




    text = extract_text(file)



    text_lower = text.lower()






    data = vectorizer.transform([text])



    result = model.predict(data)[0]




    probability = model.predict_proba(data)



    confidence = max(probability[0])*100







    found_skills=[]



    for skill in skills_list:


        if skill in text_lower:

            found_skills.append(skill)







    # ATS SCORE


    ats_score=0



    text_length=len(text_lower)





    if text_length>1500:

        ats_score+=25


    elif text_length>1000:

        ats_score+=20


    elif text_length>700:

        ats_score+=15


    elif text_length>400:

        ats_score+=10


    else:

        ats_score+=5







    skill_ratio=len(found_skills)/len(skills_list)


    ats_score += int(skill_ratio*35)







    sections=[

        "education",

        "experience",

        "project",

        "skills"

    ]



    count=0


    for section in sections:


        if section in text_lower:

            count+=1





    ats_score += count*6






    fake_keywords=[

        "years experience at age",

        "ceo at age",

        "expert in everything",

        "master of all technologies"

    ]



    for word in fake_keywords:


        if word in text_lower:

            ats_score-=20





    ats_score=max(0,min(ats_score,100))









    if result=="Real":


        reason="Resume contains realistic skills, experience and professional details."


        suggestion="Add more projects, certifications and measurable achievements."



    else:


        reason="Resume contains suspicious or unrealistic information."


        suggestion="Verify experience details and add genuine project information."









    ai_response=client.chat.completions.create(


        model="llama-3.1-8b-instant",



        messages=[


            {


                "role":"user",


                "content":f"""


Analyze this resume.



Give:

1. Strengths

2. Weaknesses

3. Improvement suggestions



Resume:


{text}


"""


            }


        ]


    )




    ai_review=(

        ai_response

        .choices[0]

        .message

        .content

    )







    return jsonify({



        "result":result,


        "confidence":round(confidence,2),


        "ats_score":ats_score,


        "skills":found_skills,


        "reason":reason,


        "suggestion":suggestion,


        "ai_review":ai_review


    })











# PDF DOWNLOAD FEATURE


@app.route("/download-report", methods=["POST"])


def download_report():



    data=request.json



    filename="AI_Resume_Report.pdf"




    doc=SimpleDocTemplate(filename)




    styles=getSampleStyleSheet()




    content=[]





    content.append(

        Paragraph(

            "AI Resume Analysis Report",

            styles["Title"]

        )

    )



    content.append(Spacer(1,20))







    content.append(

        Paragraph(

            f"Status: {data['result']}",

            styles["Normal"]

        )

    )




    content.append(

        Paragraph(

            f"Confidence: {data['confidence']}%",

            styles["Normal"]

        )

    )





    content.append(

        Paragraph(

            f"ATS Score: {data['ats_score']}%",

            styles["Normal"]

        )

    )





    content.append(

        Paragraph(

            f"Skills: {', '.join(data['skills'])}",

            styles["Normal"]

        )

    )




    content.append(

        Paragraph(

            "AI Review:",

            styles["Heading2"]

        )

    )




    content.append(

        Paragraph(

            data["ai_review"].replace("\n","<br/>"),

            styles["Normal"]

        )

    )





    content.append(

        Paragraph(

            f"Suggestions: {data['suggestion']}",

            styles["Normal"]

        )

    )






    doc.build(content)




    return send_file(

        filename,

        as_attachment=True

    )









if __name__=="__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )