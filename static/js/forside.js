
// funksjon for å laste artikler fra kategorier 
async function loadArticles(category) {
  try {
    const response = await fetch(`/get_articles/${category}`);
    const articles = await response.json();
    const container = document.getElementById("articles-container");
    container.innerHTML = "";
    articles.forEach(article => {
      // Create a preview for each article
      const articleDiv = document.createElement("div");
      articleDiv.innerHTML = `
        <h2><a href="/article/${category}/${article.id}">${article.title}</a></h2>
        <p>${article.excerpt}</p>
        <small>Published on: ${article.date_published}</small>
      `;
      container.appendChild(articleDiv);
    });
  } catch (error) {
    console.error("Error loading articles:", error);
  }
}
// Load articles from a default category
loadArticles("krim");
