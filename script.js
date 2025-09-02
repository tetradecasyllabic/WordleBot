let possible_words = null;
let gridContainer = document.getElementById("grid");

function addRow(guess, feedback) {
    for (let i = 0; i < guess.length; i++) {
        let tile = document.createElement("div");
        tile.classList.add("tile");
        let f = feedback[i];
        if (f === "🟩") tile.classList.add("green");
        else if (f === "🟨") tile.classList.add("yellow");
        else tile.classList.add("gray");
        tile.innerText = guess[i];
        gridContainer.appendChild(tile);
    }
}

async function submitGuess() {
    const guess = document.getElementById("guess").value;
    const feedback = document.getElementById("feedback").value;

    if (guess.length !== 5 || feedback.length !== 5) {
        alert("Both guess and feedback must be 5 letters!");
        return;
    }

    addRow(guess, feedback);

    const response = await fetch("/guess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guess, feedback, possible_words })
    });

    const data = await response.json();
    possible_words = data.possible_words;
    document.getElementById("next").innerText = "Next guess: " + data.next_guess;

    // Clear input for next guess
    document.getElementById("guess").value = "";
    document.getElementById("feedback").value = "";
}
