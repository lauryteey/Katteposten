async function loadFullArticle(category, articleId) {
    try {
      // Call your API endpoint
      const response = await fetch(`/api/article/${category}/${articleId}`);
  
      if (!response.ok) {
        throw new Error('Article not found');
      }
  
      const data = await response.json();
      console.log("Article data:", data);
  
      // Assume you have an element where you want to display the content
      const contentContainer = document.getElementById("article-content");
      if (contentContainer) {
        // Use innerHTML to render the content, using | safe in the template if necessary
        contentContainer.innerHTML = data.content;
      } else {
        console.error("Content container not found!");
      }
    } catch (error) {
      console.error("Error loading article content:", error);
    }
  }
  
  // Call the function with appropriate values (you can change these as needed)
  document.addEventListener("DOMContentLoaded", () => {
    // For example, load article with id 1 from category 'krim'
    loadFullArticle("krim", 1);
  });