let reportData = {};


function formatAI(text){


    return text

    .replace(/\*\*(.*?)\*\*/g,

    "<b>$1</b>")


    .replace(/(\d+\.)/g,

    "<br><b>$1</b>")


    .replace(/- /g,

    "• ")


    .replace(/â€¢/g,

    "")


    .replace(/\n+/g,

    "<br>");

}






async function checkResume(){



let file=document

.getElementById("resume")

.files[0];





if(!file){

alert("Please upload resume PDF");

return;

}





let formData=new FormData();


formData.append(

"resume",

file

);







try{



let response=await fetch(


"http://127.0.0.1:5000/check",


{


method:"POST",

body:formData


}

);






let data=await response.json();



reportData = data;








document.getElementById("result").innerHTML=




`

<div class="dashboard">





<div class="card">


<h2>
Resume Status
</h2>


<div class="status">

${data.result}

</div>


<p>

Confidence:
${data.confidence}%

</p>


</div>









<div class="card">


<h2>
ATS Score
</h2>





<div class="progress">


<div

class="progress-bar"

style="width:${data.ats_score}%">

</div>


</div>





<h1>

${data.ats_score}%

</h1>


</div>









<div class="card">


<h2>
Detected Skills
</h2>



<div class="skills">


${


data.skills.length>0


?


data.skills.map(skill=>


`

<span class="skill">

${skill}

</span>


`

).join("")



:


"No skills detected"



}



</div>


</div>









<div class="card">


<h2>
Analysis
</h2>


<p>

${data.reason}

</p>


</div>









<div class="card">


<h2>
Suggestions
</h2>


<p>

${data.suggestion}

</p>


</div>









<div class="card ai-card">


<h2>

AI Resume Review

</h2>



<div class="ai-content">


${formatAI(data.ai_review)}


</div>


<br>


<button onclick="downloadReport()">

Download Report PDF

</button>



</div>






</div>


`;




}



catch(error){


console.log(error);


alert("Server error");


}



}









async function downloadReport(){



try{



let response = await fetch(


"http://127.0.0.1:5000/download-report",


{


method:"POST",


headers:{


"Content-Type":"application/json"


},


body:JSON.stringify(reportData)


}


);






if(!response.ok){


alert("PDF creation failed");


return;


}







let blob = await response.blob();




let url = window.URL.createObjectURL(blob);




let a=document.createElement("a");



a.href=url;



a.download="Resume_Report.pdf";



document.body.appendChild(a);



a.click();



a.remove();




window.URL.revokeObjectURL(url);



}



catch(error){


console.log(error);


alert("Download failed");


}


}