// Function to fetch articles from the server
async function fetchArticles(category) {
  try {
    const response = await fetch(`/get_articles/${category}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching articles:", error);
    return [];
  }
}

// Function to create and return a new article preview element
function createArticlePreview(article, index) {
  const articleDiv = document.createElement("div");
  articleDiv.className = "articlePreview";

  // Assign class based on the article's position or content
  if (index === 0 || article.title.length > 50) {
    articleDiv.classList.add("large-article");  // Large article for first one or long titles
  } else {
    articleDiv.classList.add("small-article");  // Smaller article for others
  }

  // Insert article content into the preview
  articleDiv.innerHTML = `
    <img src="${article.previewBilde}" alt="Preview image for ${article.title}">
    <h2><a class="articlePreviewTittel" href="/article/${article.category}/${article.id}">${article.title}</a></h2>
    <p>${article.excerpt}</p>
  `;

  return articleDiv;
}

// Function to add articles to the container
function displayArticles(articles) {
  const container = document.getElementById("articles-container");
  container.innerHTML = ""; // Clear the container

  articles.forEach((article, index) => {
    const articleDiv = createArticlePreview(article, index);
    container.appendChild(articleDiv);  // Append each article preview to the container
  });
}

// Main function to load articles
async function loadArticles(category) {
  console.log("Trying to load category:", category);  // DEBUG!
  const articles = await fetchArticles(category);
  displayArticles(articles);
}

// Load articles when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  loadArticles("krim");
  loadArticles("sport");  // Load articles from the category argument having in mind this are different values (adjust as necessary)
});
