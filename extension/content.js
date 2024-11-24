// // Extract the keyword from the search URL
// function getSearchQuery() {
//   const urlParams = new URLSearchParams(window.location.search);
//   return urlParams.get("q"); // Extract the 'q' parameter
// }

// // Create a UI overlay to display the Keyword ID
// function createUIOverlay(message) {
//   let overlay = document.getElementById("keyword-overlay");

//   // If the overlay doesn't exist, create it
//   if (!overlay) {
//     overlay = document.createElement("div");
//     overlay.id = "keyword-overlay";
//     overlay.style.position = "fixed";
//     overlay.style.bottom = "20px";
//     overlay.style.right = "20px";
//     overlay.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
//     overlay.style.color = "#fff";
//     overlay.style.padding = "10px";
//     overlay.style.borderRadius = "5px";
//     overlay.style.fontSize = "14px";
//     overlay.style.zIndex = "1000";
//     document.body.appendChild(overlay);
//   }

//   // Update the overlay content
//   overlay.textContent = message;
// }

// // Send the keyword to the backend
// function sendKeywordToBackend(keyword) {
//   chrome.runtime.sendMessage({ type: "searchKeyword", keyword }, (response) => {
//     if (response.id) {
//       createUIOverlay(`Keyword Found! ID: ${response.id}`);
//     } else if (response.error) {
//       createUIOverlay(response.error);
//     }
//   });
// }

// // If on a Google search page, get the query and send it
// if (
//   window.location.hostname === "www.google.com" &&
//   window.location.pathname === "/search"
// ) {
//   const keyword = getSearchQuery();
//   if (keyword) {
//     console.log("Extracted Search Query:", keyword);
//     sendKeywordToBackend(keyword);
//   }
// }

function displayData(data) {
  let overlay = document.createElement("div");
  overlay.id = "keyword-overlay";
  overlay.style.position = "fixed";
  overlay.style.bottom = "20px";
  overlay.style.right = "20px";
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.9)";
  overlay.style.color = "#fff";
  overlay.style.padding = "10px";
  overlay.style.borderRadius = "5px";
  overlay.style.zIndex = "9999";
  overlay.style.width = "300px";
  overlay.style.overflowY = "scroll";

  // Add keyword data
  overlay.innerHTML = `
    <h3>${data["Keyword Name"]}</h3>
    <p><strong>Category:</strong> ${data["Category"]}</p>
    <p><strong>Region:</strong> ${data["Region"]}</p>
    <p><strong>Language:</strong> ${data["Language"]}</p>
    <img src="http://127.0.0.1:5000/charts/keyword_difficulty_distribution" alt="Chart" style="width: 100%; margin-top: 10px;" />
  `;

  document.body.appendChild(overlay);
}

chrome.runtime.sendMessage(
  { type: "searchKeyword", keyword: "Keyword_29" },
  (response) => {
    if (response) displayData(response);
  }
);
