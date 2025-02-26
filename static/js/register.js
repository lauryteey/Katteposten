  // Legger til en submit-hendelse for skjemaet
  document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Hindrer standard oppførsel (reload av siden)

    // Henter verdier fra inputfeltene
    const formData = {
        fornavn: document.getElementById("first-name").value,
        etternavn: document.getElementById("last-name").value,
        e_post: document.getElementById("email").value,
        passord: document.getElementById("password").value
    };

    try {
        // Sender data til serveren via POST
        const response = await fetch("/create_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (response.ok) {
            alert("Brukeren ble opprettet!"); // Bekreftelse
            window.location.href = "/"; // går til innloggingssiden
        } else {
            alert(result.error || "Kunne ikke opprette bruker."); // Feilmelding
        }
    } catch (error) {
        console.error("Feil under opprettelse av bruker:", error); // Logger feil
        alert("En feil oppsto. Vennligst prøv igjen."); // Generell feilmelding
    }
});