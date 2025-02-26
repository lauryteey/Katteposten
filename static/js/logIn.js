// Kjøres når DOM-en (HTML-siden) er ferdig lastet
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form"); // Henter login-skjemaet fra HTML
    const loginMessage = document.getElementById("login-message"); // Henter elementet for å vise login-meldinger
    const signupBtn = document.getElementById("signup-btn"); // Henter "Sign Up"-knappen fra HTML

    if (loginForm) {
        // Lytter etter innsending av skjemaet
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault(); // Hindrer standard innsending av skjemaet

            // Henter verdier fra inputfeltene for e-post og passord
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            // Sjekker om e-post og passord er fylt ut
            if (!email || !password) {
                showMessage("Vennligst fyll inn både e-post og passord.", "red"); // Viser feilmelding i rød tekst
                return; // Stopper funksjonen hvis felter mangler
            }

            try {
                // Sender login-data til serveren
                const response = await fetch("/login", {
                    method: "POST", // Bruker POST-metoden
                    headers: { "Content-Type": "application/json" }, // Angir at dataen som sendes er JSON
                    body: JSON.stringify({ e_post: email, passord: password }), // Sender e-post og passord som JSON
                });

                if (!response.ok) {
                    // Hvis login feiler, henter feilmeldingen fra serveren
                    const errorData = await response.json();
                    throw new Error(errorData.error || "Innlogging mislyktes."); // Kaster en feil med serverens melding
                }

                const result = await response.json(); // Henter suksessdata fra serveren
                window.location.href = result.redirect || "/calendar"; // Omadresserer brukeren til kalenderen
            } catch (error) {
                showMessage(error.message || "Feil e-post eller passord.", "red"); // Viser feilmeldingen i rød tekst
            }
        });
    }

    if (signupBtn) {
        // Lytter etter klikk på "Sign Up"-knappen
        signupBtn.addEventListener("click", () => {
            window.location.href = "/sign_up"; // Går til registreringssiden
        });
    }

    // Funksjon for å vise meldinger
    function showMessage(message, color) {
        if (loginMessage) {
            loginMessage.textContent = message; // Setter meldingsteksten
            loginMessage.style.color = color; // Angir fargen på meldingen
        }
    }
});