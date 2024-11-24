chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "searchKeyword") {
    fetch(
      `http://127.0.0.1:5000/search?keyword=${encodeURIComponent(
        message.keyword
      )}`
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.id) {
          sendResponse({ id: data.id, keyword: data.keyword });
        } else {
          sendResponse({ error: "Keyword not found" });
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        sendResponse({ error: "Server error. Try again later." });
      });
    return true; // Indicates the response is asynchronous
  }
});
