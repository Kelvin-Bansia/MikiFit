/*
Onderstaand script is voor een chatfunctie waarmee je kunt praten met een AI. De code werkt als volgt:

    1. Invoer ophalen: De code haalt op wat je hebt getypt in het tekstveld.
    2. Controle: Er wordt gecontroleerd of je iets hebt getypt (geen lege tekst).
    3. Jouw bericht tonen: Je bericht wordt toegevoegd aan het chatvenster.
    4. Versturen naar AI: Het bericht wordt via internet naar de server gestuurd.
    5. AI-antwoord tonen: Als de AI antwoordt, wordt het antwoord ook in het chatvenster getoond.
    6. Enter-toets: Je kunt op Enter drukken om je bericht te versturen.
*/

// Timer thinking animatie voordat error message verschijnt
const TIMEOUT_SECONDS = 60;
const TIMEOUT_MS = TIMEOUT_SECONDS * 1000;

// Wacht tot het document geladen is
$(document).ready(function() {
    // Deze functie verstuurt een bericht naar de AI
    function sendMessage() {

        // Haal de tekst op die de gebruiker heeft getypt in het invoerveld
        var userInput = $('.message-input').val().trim(); // .trim() Voor het verwijderen van witruimtes aan begin/einde

        // Controleer of er wel iets is ingetypt (en geen lege spaties)
        if (!userInput) return;

        // Voegt gebruikersbericht toe in juiste stijlformaat
        $('.chat-body').append(`
        <div class="message user-message">
            <div class="message-text">
                ${userInput}
            </div>
        </div>
        `);

        // Thinking animatie toevoegen
        $('.chat-body').append(`
            <div class="message bot-message thinking">
                <img class="bot-avatar" src="${window.BOT_AVATAR}" alt="logo chatmessage" width="50" height="50">
                <div class="message-text">
                    <div class="thinking-indicator">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
            </div>
        `);

        // Maakt het invoerveld weer leeg voor het volgende bericht
        $('.message-input').val('');

        // Timeout check
        let timeoutId = setTimeout(() => {
            if ($('.thinking').length > 0) {  // Check of thinking animatie nog bestaat
                $('.thinking').remove();
                $('.chat-body').append(`
                    <div class="message bot-message">
                        <img class="bot-avatar" src="${window.BOT_AVATAR}" alt="logo chatmessage" width="50" height="50">
                        <div class="message-text error">
                            Server reageert niet, probeer het later opnieuw.
                        </div>
                    </div>
                `);
            }
        }, TIMEOUT_MS);  // 60 seconden wachten op server response

        // verstuur het bericht naar de server via AJAX
        console.log("Before AJAX, CHAT_URL is:", window.CHAT_URL);  // Debug line
        $.ajax({
            url: window.CHAT_URL, // url chat bestaat niet meer, dus morgen ff check wat hier moet staan.
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name=csrf-token]').attr('content')
            },
            data: {
                'message': userInput
            },

            success: function(response) {
                clearTimeout(timeoutId);  // Cancel timeout als er success is
                $('.thinking').remove();  // Thinking animatie verwijderen

                // Voeg AI antwoord toe in de juiste stijlformaat
                $('.chat-body').append(`
                    <div class="message bot-message">
                        <img class="bot-avatar" src="${window.BOT_AVATAR}" alt="logo chatmessage" width="50" height="50">
                        <div class="message-text">
                            ${response.message}
                        </div>
                    </div>
                `);
        },

            // Basis error handling als het bericht niet aankomt
            error: function(error) {
                clearTimeout(timeoutId);
                $('.thinking').remove();

                console.error('Error:', error);
                $('.chat-body').append(`
                <div class="message bot-message">
                    <img class="bot-avatar" src="${window.BOT_AVATAR}" alt="logo chatmessage" width="50" height="50">
                    <div class="message-text error">
                        Er ging iets mis bij het versturen van het bericht.
                    </div>
                </div>
            `);
            }
        });
    }

    // Event listeners voor Enter toets op textarea
    $('.message-input').keypress(function(e) {
        if (e.which == 13 && !e.shiftKey) {  // Voorkom trigger bij Shift+Enter
            e.preventDefault();
            sendMessage();
        }
    });

    // Voor submit button
    $('.chat-form').submit(function(e) {
        e.preventDefault();
        sendMessage();
    });
});
