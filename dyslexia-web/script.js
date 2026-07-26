"use strict";
const API_URL = "https://dyslexia-chatbot.onrender.com";
const questionInput = document.getElementById("question");
const askButton = document.getElementById("ask-button");
const loading = document.getElementById("loading");
const error = document.getElementById("error");
const result = document.getElementById("result");
const answer = document.getElementById("answer");
const sources = document.getElementById("sources");
askButton.addEventListener("click", askQuestion);
async function askQuestion() {
    const question = questionInput.value.trim();
    if (!question) {
        return;
    }
    loading.hidden = false;
    error.hidden = true;
    result.hidden = true;
    askButton.disabled = true;
    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });
        if (!response.ok) {
            throw new Error("API request failed");
        }
        const data = await response.json();
        displayResult(data);
    }
    catch (err) {
        console.error(err);
        error.textContent =
            "Something went wrong. Please try again.";
        error.hidden = false;
    }
    finally {
        loading.hidden = true;
        askButton.disabled = false;
    }
}
function displayResult(data) {
    answer.textContent = data.answer;
    sources.innerHTML = "";
    for (const source of data.sources) {
        const link = document.createElement("a");
        link.href = source.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent =
            `${source.title} - ${source.section ?? "Website"}`;
        sources.appendChild(link);
        sources.appendChild(document.createElement("br"));
    }
    result.hidden = false;
}
