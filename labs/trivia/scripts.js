multipleChoice(["#btn1"], ["#btn2", "#btn3"], "#feedback1");
freeResponse("#freeResponse", "#Q2", "#feedback2", ["js", "html", "css"]);

async function multipleChoice(correctElems, incorrectElems, feedback) {
  var timesAnswered = 0;

  document.addEventListener("DOMContentLoaded", async () => {
    // Loop through the correct elements and set an event listner for each one
    correctElems.map((i) => {
      document.querySelector(i).addEventListener("click", async () => {
        await reset();

        // Set the backgound color to green to give the user the idea of being correct
        document.querySelector(i).style.backgroundColor = "green";
        document.querySelector(i).style.color = "white";

        // If the user didn't get the hint that they were correct, explicitly say it below
        document.querySelector(feedback).style.color = "green";
        document.querySelector(feedback).innerHTML = "Correct! 😊";
      });
    });

    incorrectElems.map((i) => {
      document.querySelector(i).addEventListener("click", async () => {
        await reset();

        // Set the backgound color to red to give the user the idea of being incorrect
        document.querySelector(i).style.backgroundColor = "red";
        document.querySelector(i).style.color = "white";

        // If the user didn't get the hint that they were incorrect, explicitly say it below
        document.querySelector(feedback).style.color = "red";
        document.querySelector(feedback).innerHTML = "Incorrect! 😔";
      });
    });
  });
  async function reset() {
    // Cheat detection
    timesAnswered += 1;
    if (timesAnswered >= 8)
      alert("😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡");
    else if (timesAnswered >= 6) alert("STOP CHEATING 😡");
    else if (timesAnswered >= 4) alert("STOP CHEATING 😠");
    else if (timesAnswered >= 2) alert("Please Stop Cheating");

    // Reset the feedback for the multiple choice question
    document.querySelector(feedback).style.color = "black";
    document.querySelector(feedback).innerHTML = "";

    // Reset the colors of the button
    correctElems.concat(incorrectElems).map((i) => {
      document.querySelector(i).style.backgroundColor = "#d9edff";
      document.querySelector(i).style.color = "black";
    });
  }
}

async function freeResponse(submitButton, input, feedback, correctAnswers) {
  document.addEventListener("DOMContentLoaded", async () => {
    document.querySelector(submitButton).addEventListener("click", async () => {
      if (
        correctAnswers.includes(
          document.querySelector(input).value.toString().toLowerCase()
        )
      ) {
        // Set the backgound color to green to give the user the idea of being correct
        document.querySelector(input).style.backgroundColor = "green";
        document.querySelector(input).style.color = "white";

        // If the user didn't get the hint that they were correct, explicitly say it below
        document.querySelector(feedback).style.color = "green";
        document.querySelector(feedback).innerHTML = "Correct! 😊";
      } else {
        // Set the backgound color to red to give the user the idea of being incorrect
        document.querySelector(input).style.backgroundColor = "red";
        document.querySelector(input).style.color = "white";

        // If the user didn't get the hint that they were incorrect, explicitly say it below
        document.querySelector(feedback).style.color = "red";
        document.querySelector(feedback).innerHTML = "Incorrect! 😔";
      }
    });
  });
}
