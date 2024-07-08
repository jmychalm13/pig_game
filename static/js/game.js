document.addEventListener("DOMContentLoaded", () => {
  const rollButton = document.getElementById("roll-button");
  const endTurnButton = document.getElementById("end-turn-button");
  const gameStatus = document.getElementById("game-status");
  const currentPlayerScore = document.getElementById("current-player-score");
  const diceImage = document.getElementById("dice-image");
  const currentPlayerDisplay = document.getElementById("current-player");

  function updatePlayerScores(scores) {
    for (let i = 0; i < scores.length; i++) {
      const playerScoreElement = document.getElementById(`player${i + 1}-score`);
      if (playerScoreElement) {
        playerScoreElement.textContent = scores[i];
      }
    }
    // console.log(scores);
  }

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
          currentPlayerScore.textContent = data.current_score;
          diceImage.src = `/static/img/inverted-dice-${data.value}.png`;
          currentPlayerDisplay.textContent = data.current_player + 1;
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
        if (data.winner !== undefined && data.winner !== null) {
          gameStatus.textContent = `Player ${data.winner + 1} wins with a score of ${data.scores[data.winner]}!`;
          rollButton.disabled = true;
          endTurnButton.disabled = true;
        } else {
          console.log(data);
          // gameStatus.textContent = `Next player: Player ${data.next_player + 1}`;
          rollButton.disabled = false;
          endTurnButton.disabled = false;
          currentPlayerDisplay.textContent = data.current_player + 1;
          currentPlayerScore.textContent = `0`;
          updatePlayerScores(data.scores);
        }
      })
      .catch((error) => {
        console.error("Error", error);
      });
  });
});
