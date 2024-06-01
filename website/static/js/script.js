document.getElementById('scraping-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const keyword = document.getElementById('keyword').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const nombreIter = document.getElementById('nombre-iter').value;
    
    document.getElementById('loading').style.display = 'block';

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/scrape', true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                window.location.href = '/result';
            } else {
                console.error('Error:', xhr.statusText);
            }
        }
    };
    
    xhr.send(JSON.stringify({ keyword: keyword, start_date: startDate, end_date: endDate, nombre_iter: nombreIter }));
});
