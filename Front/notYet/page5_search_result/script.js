document.querySelector('#search-button').addEventListener('click', function(event) {
    event.preventDefault(); // prevent the default action

    // get the search term from the input field
    var searchTerm = document.querySelector('#search-input').value;
    
    fetch('/search?term=' + searchTerm)
        .then(response => response.json())
        .then(data => {
            // clear previous search results
            var resultContainer = document.querySelector('.result-container');
            resultContainer.innerHTML = '';
            
            // display search term and search image at the top
            var searchTextElement = document.createElement('h2');
            searchTextElement.textContent = `Top 5 Products similar with "${data.searchText}"`;
            resultContainer.appendChild(searchTextElement);
            
            if(data.searchImage !== "") {
                var searchImageElement = document.createElement('img');
                searchImageElement.src = data.searchImage;
                resultContainer.appendChild(searchImageElement);
            }

            // display new search results
            data.products.forEach(product => {
                var productElement = document.createElement('div');
                productElement.classList.add('product');
                
                var imageElement = document.createElement('img');
                imageElement.src = product.productImage;
                productElement.appendChild(imageElement);
                
                var nameElement = document.createElement('h3');
                nameElement.textContent = product.productName;
                productElement.appendChild(nameElement);

                var bigcatElement = document.createElement('span');
                bigcatElement.textContent = product.productBigcat;
                bigcatElement.classList.add('bigcat-tag');
                productElement.appendChild(bigcatElement);

                var smallcatElement = document.createElement('span');
                smallcatElement.textContent = product.productSmallcat;
                smallcatElement.classList.add('smallcat-tag');
                productElement.appendChild(smallcatElement);

                product.productHashtag.forEach(hashtag => {
                    var hashtagElement = document.createElement('span');
                    hashtagElement.textContent = hashtag;
                    hashtagElement.classList.add('hashtag-tag');
                    productElement.appendChild(hashtagElement);
                });

                var productLinkElement = document.createElement('a');
                productLinkElement.href = product.productUrl;
                productLinkElement.textContent = "Go to the product page";
                productElement.appendChild(productLinkElement);
                
                resultContainer.appendChild(productElement);
            });

            // 검색 결과 섹션 표시하기
            document.getElementById('search-results').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
