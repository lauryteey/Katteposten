// Function to load a full article from the server
async function loadFullArticle(category, articleId) {
  try {
    // Make a request to your API to get the full article
    const response = await fetch(`/api/article/${category}/${articleId}`);

    // If the response is not OK (e.g. 404), throw an error
    if (!response.ok) {
      throw new Error('Article not found');
    }

    // Convert the response to JSON
    const data = await response.json();
    console.log("Article data:", data); // For debugging

    // Find the element where the article content should be displayed
    const contentContainer = document.getElementById("article-content");

    // If the container is found, insert the article content into it
    if (contentContainer) {
      // Render the article content assuming it's HTML
      contentContainer.innerHTML = data.content;
    } else {
      // If the container is missing in the HTML
      console.error("Content container not found!");
    }
  } catch (error) {
    // Show any errors that happened while loading the article
    console.error("Error loading article content:", error);
  }
}


// Run this when the page has finished loading
document.addEventListener("DOMContentLoaded", () => {
  // get the article ID from the URL
  loadFullArticle("krim", 1);
});
