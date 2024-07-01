document.addEventListener("DOMContentLoaded", () => {
  const rollButton = document.getElementById("roll-button");
  const endTurnButton = document.getElementById("end-turn-button");
  const gameStatus = document.getElementById("game-status");
  const gameOutput = document.getElementById("game-output");
  const diceImage = document.getElementById("dice-image");

  rollButton.addEventListener("click", () => {
    fetch("/roll-dice", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        gameOutput.textContent = `You rolled a ${data.value}`;
        if (data.value === 1) {
          gameStatus.textContent = `You rolled a 1! Turn done! Current score: 0`;
        } else {
          gameStatus.textContent = `Current score: ${data.current_score}`;
        }
        diceImage.src = `/static/img/inverted-dice-${data.value}.png`;
      });
  });
  endTurnButton.addEventListener("click", () => {
    fetch("/end-turn", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.winner) {
          gameStatus.textContent = `Player ${data.winner} wins with a score of ${data.score}!`;
          rollButton.disabled = true;
          endTurnButton.disabled = true;
        } else {
          gameStatus.textContent = `Next player: ${data.next_player}`;
          gameOutput.textContent = "";
        }
      });
  });
});
