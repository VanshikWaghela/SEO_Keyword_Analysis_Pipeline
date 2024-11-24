document.getElementById("searchButton").addEventListener("click", function () {
  var keyword = document.getElementById("keyword").value;

  if (keyword) {
    // Send the request to the Flask backend
    fetch(
      `http://localhost:5000/search?keyword=${encodeURIComponent(keyword)}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        var resultDiv = document.getElementById("result");
        var resultMessage = document.getElementById("resultMessage");

        if (data.id) {
          // Keyword found
          resultDiv.style.display = "block";
          resultDiv.classList.remove("not-found");
          resultDiv.classList.add("found");
          resultMessage.textContent = `Keyword Found! ID: ${data.id}`;
        } else {
          // Keyword not found
          resultDiv.style.display = "block";
          resultDiv.classList.remove("found");
          resultDiv.classList.add("not-found");
          resultMessage.textContent = "Keyword not found";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});
