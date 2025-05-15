// Function to fetch articles to the server
async function fetchArticles(category) {
  try {
    const endpoint = category === 'all' ? '/get_articles/all' : `/get_articles/${category}`;
    const response = await fetch(endpoint);
    const data = await response.json();
    return data.articles || data;  // returns array directly
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
  const message = document.getElementById("no-articles-message");

  container.innerHTML = ""; // Tøm artiklene

  if (!articles || articles.length === 0) {
    message.style.display = "block";
    message.textContent = "Hmm... ser ut som at det ikke finnes katteartikler her 🐾";
    return;
  }

  // Hvis det finnes artikler, skjul meldingen
  message.style.display = "none";

  articles.forEach((article, index) => {
    const articleDiv = createArticlePreview(article, index);
    container.appendChild(articleDiv);
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
  const params = new URLSearchParams(window.location.search);
  const category = params.get("category") || "all";
  loadArticles(category);

  const buttons = document.querySelectorAll(".category-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const category = button.getAttribute("data-category");
      loadArticles(category);
    });
  });
});

