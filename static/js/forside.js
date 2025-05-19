// Function to fetch articles from the server
async function fetchArticles(category) {
  try {
    // Choose the correct endpoint depending on the category
    const endpoint = category === 'all' ? '/get_articles/all' : `/get_articles/${category}`;

    // Send a request to the server
    const response = await fetch(endpoint);

    // Convert the response to JSON
    const data = await response.json();

    // Return the array of articles (or just data if it's already an array)
    return data.articles || data;
  } catch (error) {
    // Show an error message if something goes wrong
    console.error("Error fetching articles:", error);
    return []; // Return an empty array if there was a problem
  }
}


// Function to create and return a new article preview element
function createArticlePreview(article, index) {
  // Make a new div for this article
  const articleDiv = document.createElement("div");
  articleDiv.className = "articlePreview";

  // Add an extra class if it's the first article or has a long title
  if (index === 0 || article.title.length > 50) {
    articleDiv.classList.add("large-article");
  } else {
    articleDiv.classList.add("small-article");
  }

  // Fill the div with article content: image, title (as a link), and excerpt
  articleDiv.innerHTML = `
    <img src="${article.previewBilde}" alt="Preview image for ${article.title}">
    <h2><a class="articlePreviewTittel" href="/article/${article.category}/${article.id}">${article.title}</a></h2>
    <p>${article.excerpt}</p>
  `;

  // Return the finished article element
  return articleDiv;
}


// Function to add articles to the HTML container
function displayArticles(articles) {
  // Find the container for the articles and the message element
  const container = document.getElementById("articles-container");
  const message = document.getElementById("no-articles-message");

  // Clear out any old content
  container.innerHTML = "";
  message.style.display = "none"; // Hide the "no articles" message at first

  // If there are no articles, show a message to the user
  if (!articles || articles.length === 0) {
    message.style.display = "block";
    message.textContent = "Hmm... ser ut som at det ikke finnes katteartikler her 🐾";
    return;
  }

  // Go through each article and add it to the container
  articles.forEach((article, index) => {
    const articleDiv = createArticlePreview(article, index);
    container.appendChild(articleDiv);
  });
}


// Main function to load articles for a specific category
async function loadArticles(category) {
  // Hide the "no articles" message in case it was shown earlier
  const message = document.getElementById("no-articles-message");
  message.style.display = "none";

  // Print which category we're loading (for debugging)
  console.log("Trying to load category:", category);

  // Get articles from the server and display them
  const articles = await fetchArticles(category);
  displayArticles(articles);
}


// Run this when the page has finished loading
document.addEventListener("DOMContentLoaded", () => {
  // Check if there's a category in the URL (e.g., ?category=news)
  const params = new URLSearchParams(window.location.search);
  const category = params.get("category") || "all"; // Use "all" if no category

  // Load the articles for that category
  loadArticles(category);

  // Add event listeners to all category buttons
  const buttons = document.querySelectorAll(".category-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      // When a button is clicked, get its category and load the articles
      const category = button.getAttribute("data-category");
      loadArticles(category);
    });
  });
});
