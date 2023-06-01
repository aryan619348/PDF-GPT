async function processPDF() {
    const fileLink = document.getElementById("fileLink").value;
    const question = document.getElementById("question").value;

    const data = {
        file_link: fileLink,
        question: question
    };

    const response = await fetch('/process_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    const answer = result.answer;

    document.getElementById("answerContainer").innerText = "Answer: " + answer;
}
