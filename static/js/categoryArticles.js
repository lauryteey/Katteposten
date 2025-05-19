// Wait until the whole page has loaded
document.addEventListener("DOMContentLoaded", () => {

  // Find all elements with the class "category-link"
  document.querySelectorAll('.category-link').forEach(link => {

    // When a category link is clicked
    link.addEventListener('click', (e) => {
      console.log("category link clicked");

      // Stop the link from going to a new page
      e.preventDefault();

      // Get the category name from the link's data attribute
      const category = link.dataset.category;

      // Send a request to the server to get the articles for that category
      fetch(`/get_articles/${category}`)
        .then(res => res.json()) // Convert the response to JSON
        .then(articles => {
          // Find the container where articles will be shown
          const container = document.getElementById('articles-container');

          // Clear any old articles from the container
          container.innerHTML = '';

          // Go through each article and add it to the page
          articles.forEach(article => {
            const div = document.createElement('div');

            // Set the HTML content for this article
            div.innerHTML = `
              <h2>${article.title}</h2>
              <p>Publisert: ${article.date_published}</p>
              <a href="/article/${article.category}/${article.id}">Les mer</a>
            `;

            // Add the article to the container
            container.appendChild(div);
          });
        })
        .catch(err => {
          // If there is an error, show it in the console
          console.error("Feil med å hente artikler:", err);
        });
    });
  });
});
