document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("guestbookForm");
    const nameInput = document.getElementById("name");
    const message = document.getElementById("confirmationMessage");
    const tableBody = document.getElementById("guestbookBody");

    // Fetch and render entries
    function loadEntries() {
        fetch("/guestbook/entries")
            .then(res => res.json())
            .then(data => {
                tableBody.innerHTML = "";
                data.forEach(person => {
                    const row = document.createElement("tr");
                    row.innerHTML = `<td>${person.id}</td><td>${person.name}</td>`;
                    tableBody.appendChild(row);
                });
            });
    }

    // Handle form submission
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = nameInput.value;

        fetch("/guestbook", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        })
        .then(res => res.json())
        .then(data => {
            message.textContent = `Added: ${data.name}`;
            nameInput.value = "";
            loadEntries(); // Refresh table
        })
        .catch(err => {
            message.textContent = "Error adding entry.";
            console.error(err);
        });
    });

    loadEntries(); // Initial load
});