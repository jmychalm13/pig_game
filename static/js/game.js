document.addEventListener("DOMContentLoaded", () => {
  const rollButton = document.getElementById("roll-button");
  const endTurnButton = document.getElementById("end-turn-button");
  const gameStatus = document.getElementById("game-status");
  const gameOutput = document.getElementById("game-output");
  const diceImage = document.getElementById("dice-image");
  const currentPlayerDisplay = document.getElementById("current-player");

  rollButton.addEventListener("click", () => {
    fetch("/roll-dice", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.value === 1) {
          gameStatus.textContent = `You rolled a 1!`;
          rollButton.disabled = true;

          endTurnButton.disabled = false;
        } else {
          gameStatus.textContent = `You rolled a ${data.value}`;
          currentPlayerDisplay.textContent = `Current Player: ${data.current_player + 1}`;
        }
      })
      .catch((error) => {
        console.error("Error", error);
      });
  });

  endTurnButton.addEventListener("click", () => {
    fetch("/end-turn", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.winner) {
          gameStatus.textContent = `Player ${data.winner + 1} wins with a score of ${data.score}!`;
          rollButton.disabled = true;
          endTurnButton.disabled = true;
        } else {
          gameStatus.textContent = `Next player: Player ${data.next_player + 1}`;
          rollButton.disabled = false;
          endTurnButton.disabled = false;
          currentPlayerDisplay.textContent = `Current Player: Player ${data.current_player + 1}`;
        }
      })
      .catch((error) => {
        console.error("Error", error);
      });
  });
});
