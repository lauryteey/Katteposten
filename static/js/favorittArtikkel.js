function leggTilFavoritt(id, kategori, tittel) {
    fetch('/leggtil_favoritt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ article_id: id, category: kategori, title: tittel })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else if (data.error) {
                alert(data.error);
            } else {
                alert("Ukjent svar fra serveren.");
            }
        })
        .catch(err => alert("Noe gikk galt!"));
}
