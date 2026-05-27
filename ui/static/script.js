async function askQuestion() {

    const question = document.getElementById("questionInput").value;
    const modelChoice = document.getElementById("modelSelect").value;

    const ragBox = document.getElementById("ragAnswer");

    const agenticBox = document.getElementById("agenticAnswer");

    ragBox.innerHTML = "Generating answer...";

    agenticBox.innerHTML = "Thinking deeply...";

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: question,
                model_choice: modelChoice
            })

        });

        const data = await response.json();

        // ragBox.innerHTML = data.rag_answer;

        // Parse Markdown
        const ragParsed = marked.parse(data.rag_answer);
        const agenticParsed = marked.parse(data.agentic_answer);

        // Build Metrics HTML for RAG
        let ragMetricsHTML = '<div class="mt-4"><div class="mb-2 font-bold text-blue-300">Evaluation Metrics:</div><ul class="text-sm text-gray-300 space-y-1">';
        if (data.rag_metrics) {
            for (const [key, value] of Object.entries(data.rag_metrics)) {
                // Ensure visual display as percentage
                const percentage = (value * 100).toFixed(0);
                ragMetricsHTML += `<li><span class="font-semibold text-gray-200">${key}:</span> <span class="text-blue-400">${percentage}%</span></li>`;
            }
        }
        ragMetricsHTML += '</ul></div>';

        // Build Metrics HTML for Agentic
        let agenticMetricsHTML = '<div class="mt-4"><div class="mb-2 font-bold text-purple-300">Evaluation Metrics:</div><ul class="text-sm text-gray-300 space-y-1">';
        if (data.agentic_metrics) {
            for (const [key, value] of Object.entries(data.agentic_metrics)) {
                // Ensure visual display as percentage
                const percentage = (value * 100).toFixed(0);
                agenticMetricsHTML += `<li><span class="font-semibold text-gray-200">${key}:</span> <span class="text-purple-400">${percentage}%</span></li>`;
            }
        }
        agenticMetricsHTML += '</ul></div>';

        ragBox.innerHTML = `
            <div class="mb-2 font-bold">Answer:</div>
            <div class="markdown-content">${ragParsed}</div>

            <br>

            <div class="mb-2 font-bold">Sources:</div>
            <p class="text-sm text-gray-400">${data.rag_sources.join("<br>")}</p>

            <hr class="my-4 border-gray-700">
            ${ragMetricsHTML}
            `;

        agenticBox.innerHTML = `
            <div class="mb-2 font-bold">Answer:</div>
            <div class="markdown-content">${agenticParsed}</div>

            <br>

            <div class="mb-2 font-bold">Rewritten Queries:</div>
            <p class="text-sm text-gray-400">${data.rewritten_queries.join("<br>")}</p>

            <br>

            <div class="mb-2 font-bold">Sources:</div>
            <p class="text-sm text-gray-400">${data.agentic_sources.join("<br>")}</p>

            <hr class="my-4 border-gray-700">
            ${agenticMetricsHTML}
            `;

    }

    catch (error) {

        ragBox.innerHTML = "Error generating response.";

        agenticBox.innerHTML = "Error generating response.";

        console.error(error);
    }
}