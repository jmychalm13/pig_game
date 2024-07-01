function rollDice() {
  fetch("/roll-dice", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      const output = document.getElementById("game-output");
      output.innerHTML = data.message;
    })
    .catch((error) => console.error("Error", error));
}

function endTurn() {
  fetch("/end-turn", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      const output = document.getElementById("game-output");
      output.innerHTML = data.message;
    })
    .catch((error) => console.error("Error:", error));
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("roll-button").addEventListener("click", rollDice);
  document.getElementById("end-turn-button").addEventListener("click", endTurn);
});
