document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const generateSummaryButton = document.getElementById("generate-summary-btn");
    const downloadLink = document.getElementById("download-transcript");
    const summaryElement = document.getElementById("summary");
    
    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        
        const audioFile = document.getElementById("audio-file").files[0];
        const uploadSuccessMsg = document.getElementById("upload-success-msg");
    
        if (!audioFile) {
            alert("Please choose an audio file.");
            return;
        }
    
  
        const formData = new FormData();
        formData.append("file", audioFile);
    
        downloadLink.style.display = "none";
        uploadSuccessMsg.style.display = "block";
    
        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });
    
            if (response && response.ok) {
                const data = await response.json();
                const transcriptBlob = new Blob([data.transcript_text], { type: "text/plain" });
                const transcriptUrl = URL.createObjectURL(transcriptBlob);
                
                console.log(`Received!${data.transcript_text}`)


                downloadLink.href = transcriptUrl;
                downloadLink.style.display = "block";
                summaryElement.value = "";
                generateSummaryButton.disabled = false;
            } else if (response) {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
                summaryElement.value = "";
                downloadLink.style.display = "none";
            } else {
                alert("An unexpected error occurred.");
                summaryElement.value = "";
                downloadLink.style.display = "none";
            }
        } catch (error) {
            console.error(error);
            alert("An unexpected error occurred.");
            summaryElement.value = "";
            downloadLink.style.display = "none";
        }
    });

    generateSummaryButton.addEventListener("click", async () => {
        const transcriptUrl = downloadLink.href;
        const transcriptResponse = await fetch(transcriptUrl);
        const transcriptText = await transcriptResponse.text();

        summaryElement.value = "Generating summary...";

        try {
            const summaryResponse = await fetch("/summarize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ transcript: transcriptText }),
            });

            if (summaryResponse && summaryResponse.ok) {
                const summaryData = await summaryResponse.json();
                summaryElement.value = summaryData.summary;
            } else if (summaryResponse) {
                const errorData = await summaryResponse.json();
                alert(`Error: ${errorData.error}`);
                summaryElement.value = "";
            } else {
                alert("An unexpected error occurred.");
                summaryElement.value = "";
            }
        } catch (error) {
            console.error(error);
            alert("An unexpected error occurred.");
            summaryElement.value = "";
        }
    });

    async function copyToClipboard(text) {
        const tempTextArea = document.createElement("textarea");
        tempTextArea.value = text;
        document.body.appendChild(tempTextArea);
        tempTextArea.focus();
        tempTextArea.select();
        try {
            document.execCommand("copy");
        } catch (error) {
            alert("Failed to copy text: " + error);
        } finally {
            document.body.removeChild(tempTextArea);
        }
    }

    document.getElementById("copy-btn-callnotes").addEventListener("click", () => {
        const outputText = document.getElementById("summary").value;
        copyToClipboard(outputText);
        alert("Summary copied to clipboard.");
    });
});
