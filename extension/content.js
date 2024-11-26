function getSearchKeyword() {
  // Extract the keyword from the page's search input field or URL
  let keyword = "";

  // Try to extract keyword from a common search field
  const searchInput = document.querySelector("input[type='text'], input[type='search']");
  if (searchInput) {
      keyword = searchInput.value.trim();
  }

  // If the search input is empty, try extracting it from the URL
  if (!keyword) {
      const urlParams = new URLSearchParams(window.location.search);
      keyword = urlParams.get("q") || ""; // Common for Google or search pages
  }

  return keyword;
}

function displayData(data, suggestions) {
  let overlay = document.createElement("div");
  overlay.id = "keyword-overlay";
  overlay.style.position = "fixed";
  overlay.style.bottom = "20px";
  overlay.style.right = "20px";
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.9)";
  overlay.style.color = "#fff";
  overlay.style.padding = "20px"; // Increased padding
  overlay.style.borderRadius = "10px"; // More rounded corners
  overlay.style.zIndex = "9999";
  overlay.style.width = "400px"; // Increased width
  overlay.style.height = "500px"; // Increased height
  overlay.style.overflowY = "scroll";
  overlay.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.5)"; // Add shadow for depth

  if (data.error) {
      overlay.innerHTML = `<p>Error: ${data.error}</p>`;
  } else {
      // Main keyword details
      let htmlContent = `
          <h3>${data["Keyword Name"]}</h3>
          <p><strong>Category:</strong> ${data["Category"]}</p>
          <p><strong>Region:</strong> ${data["Region"]}</p>
          <p><strong>Language:</strong> ${data["Language"]}</p>
          <p><strong>CPC:</strong> ${data["CPC (Cost Per Click)"]}</p>
          <p><strong>Search Volume:</strong> ${data["Search Volume"]}</p>
          <p><strong>Monthly Trend Chart of keyword:</strong></p>
          <img src="http://127.0.0.1:5000/charts/${data["Keyword Name"]}/trends" alt="Trend Chart" style="width: 100%; margin-top: 10px;" />
          
      `;

      // Suggested keywords section
      if (suggestions && suggestions.length > 0) {
          htmlContent += `<h4>Suggested Keywords</h4><ul>`;
          suggestions.forEach(suggestion => {
              htmlContent += `<li>${suggestion}</li>`;
          });
          htmlContent += `</ul>`;
      }

      overlay.innerHTML = htmlContent;
  }

  document.body.appendChild(overlay);
}
  


// Function to fetch data from Flask API
function fetchKeywordData(keywordName) {
  fetch(`http://127.0.0.1:5000/keyword/${keywordName}`)
      .then(response => response.json())
      .then(data => {
          displayData(data, data.suggestions || []);
      })
      .catch(error => {
          console.error("Error fetching keyword data:", error);
      });
}


// Extract keyword and fetch data
const searchKeyword = getSearchKeyword();
if (searchKeyword) {
  fetchKeywordData(searchKeyword);
} else {
  console.log("No keyword found on this page.");
}
