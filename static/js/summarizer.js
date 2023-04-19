document.getElementById("clear-content").addEventListener("click", () => {
  const inputTextarea = document.getElementById("input-text");
  inputTextarea.value = "";
});

function showGeneratingSummaryMessage() {
  const outputTextEn = document.getElementById("output-text-en");
  const outputTextCn = document.getElementById("output-text-cn");

  outputTextEn.value = "Generating summary...";
  outputTextCn.value = "Generating summary...";
}

document.getElementById("summary").addEventListener("click", async () => {
  const inputText = document.getElementById("input-text");
  const outputTextEn = document.getElementById("output-text-en");
  const outputTextCn = document.getElementById("output-text-cn");

  showGeneratingSummaryMessage();
  if (inputText.value.trim() !== "") {
    // Fetch the summary
    const response = await fetch("/summarizer/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: inputText.value }),
    });
    const summary = await response.text();
    outputTextEn.value = summary;

    // Fetch the translation
    const translationResponse = await fetch("/summarizer/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: summary }),
    });
    const translation = await translationResponse.text();
    outputTextCn.value = translation;
  } else {
    alert("Please paste your original news.");
  }
});

document.getElementById("copy-btn-summary-en").addEventListener("click", () => {
  const summaryTextarea = document.getElementById("output-text-en");

  if (summaryTextarea.value.trim() !== "") {
    summaryTextarea.select();
    summaryTextarea.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("English summary copied to clipboard.");
  } else {
    alert("No English summary to copy.");
  }
});

document.getElementById("copy-btn-summary-cn").addEventListener("click", () => {
  const summaryTextarea = document.getElementById("output-text-cn");

  if (summaryTextarea.value.trim() !== "") {
    summaryTextarea.select();
    summaryTextarea.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Chinese summary copied to clipboard.");
  } else {
    alert("No Chinese summary to copy.");
  }
});
