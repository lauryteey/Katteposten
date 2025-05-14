// This fucntion fetches the aricles from a specific category when the user clicks on a category link
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.category-link').forEach(link => {
    link.addEventListener('click', (e) => {
      console.log("category link e called");

      e.preventDefault();
      const category = link.dataset.category;

      fetch(`/get_articles/${category}`)
        .then(res => res.json())
        .then(articles => {
          const container = document.getElementById('articles-container');
          container.innerHTML = ''; // Clear previous articles

          articles.forEach(article => {
            const div = document.createElement('div');
            div.innerHTML = `
              <h2>${article.title}</h2>
              <p>Publisert: ${article.date_published}</p>
              <a href="/article/${article.category}/${article.id}">Les mer</a>
            `;
            container.appendChild(div);
          });
        })
        .catch(err => console.error("Feil med å hente artikler:", err));
    });
  });
});
