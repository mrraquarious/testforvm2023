document.addEventListener("DOMContentLoaded", () => {
    async function translateText(text, sourceLang, targetLang) {
        console.log('Input text:', text);
        console.log('Source language:', sourceLang);
        console.log('Target language:', targetLang);

        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, sourceLang, targetLang })
        });

        if (response.ok) {
            const data = await response.json();
            console.log('API response:', data);
            return data.translated_text;
        } else {
            throw new Error('Error: ' + response.statusText);
        }
    }

    document.getElementById("translation").addEventListener("click", async () => {
        const text = document.getElementById("input-text").value;
        if (!text) return;
        const langSelection = document.getElementById("lang-selection").value;
        const [sourceLang, targetLang] = langSelection.split("-");
    
        const outputElement = document.getElementById("output-text");
    
        outputElement.innerText = "Generating translation...";
    
        try {
            const translatedText = await translateText(text, sourceLang, targetLang);
            outputElement.innerText = translatedText;
        } catch (error) {
            console.error(error);
            alert('An error occurred while processing the translation. Please try again.');
        } finally {
            translationElement.innerText = "Translate";
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

    document.getElementById("copy-btn-translation").addEventListener("click", () => {
        const outputText = document.getElementById("output-text").value;
        copyToClipboard(outputText);
        alert("Translation copied to clipboard.");
    });

});
