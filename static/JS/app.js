// Add Rule (Supports both GET and POST methods)
function addRule() {
    const rule = document.getElementById("rule-input").value;

    // If rule is provided, use POST method
    if (rule) {
        fetch('/rules', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rule: rule })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("add-rule-response").innerText = data.message || data.error;
        })
        .catch(error => console.error('Error:', error));
    } else {
        // If no rule is provided, use GET method
        fetch('/rules', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("add-rule-response").innerText = `GET Response: ${data.message || data.error}`;
        })
        .catch(error => console.error('Error:', error));
    }
}
function evaluateRule() {
    const ruleId = document.getElementById("rule-id-input").value;
    const dataInput = document.getElementById("data-input").value;

    let data;
    try {
        data = JSON.parse(dataInput); // Ensure this is a valid JSON object
    } catch (e) {
        console.error("Invalid JSON input:", e);
        document.getElementById("evaluate-rule-response").innerText = "Invalid JSON input.";
        return;
    }

    // Check if ruleId and data are present
    if (ruleId && data) {
        fetch('/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                rule_id: ruleId,
                data: data
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error);
                });
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("evaluate-rule-response").innerText = `Result: ${data.result}`;
        })
        .catch(error => {
            document.getElementById("evaluate-rule-response").innerText = `Error: ${error.message}`;
            console.error('Error:', error);
        });
    } else {
        // If ruleId or data isn't provided, make a GET request
        fetch(`/evaluate?rule_id=${ruleId}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("evaluate-rule-response").innerText = `GET Response: ${data.result || data.error}`;
        })
        .catch(error => console.error('Error:', error));
    }
}



// Delete Rule (Remains unchanged with DELETE method)
function deleteRule() {
    const ruleId = document.getElementById("delete-rule-id").value;

    fetch(`/rules/${ruleId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("delete-rule-response").innerText = data.message || data.error;
    })
    .catch(error => console.error('Error:', error));
}
