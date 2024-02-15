const header = document.querySelector("header");
const hamburgerBtn = document.querySelector("#hamburger-btn");
const closeMenuBtn = document.querySelector("#close-menu-btn");

// Toggle mobile menu on hamburger button click
hamburgerBtn.addEventListener("click", () => header.classList.toggle("show-mobile-menu"));

// Close mobile menu on close button click
closeMenuBtn.addEventListener("click", () => hamburgerBtn.click());


// HTML 요소에 대한 참조를 가져옵니다.
var searchInput = document.getElementById("searchQuery"),
    searchButton = document.getElementById("searchButton"); // 이 버튼 ID는 HTML에서 설정해야 합니다.

// 'Search' 버튼에 대한 클릭 이벤트 리스너를 추가합니다.
// HTML 내에서 onclick 속성 대신 이 방식을 사용할 수 있습니다.
// 이를 위해 HTML에서 <button> 요소에 id="searchButton"을 추가해야 합니다.
searchButton.addEventListener("click", searchImages);

function searchImages() {
    var searchQuery = document.getElementById('searchQuery').value; 

    // 로딩 페이지를 표시합니다.
    document.getElementById('loadingPage').style.display = 'block'; 

    // 검색창을 숨깁니다.
    document.getElementById('searchSection').style.display = 'none';

    // XMLHttpRequest 객체를 생성합니다.
    var xhr = new XMLHttpRequest();

    // 요청을 초기화합니다.
    xhr.open('POST', 'http://165.132.46.86:32073/textSearch', true);

    // 요청 헤더를 설정합니다.
    xhr.setRequestHeader('Content-Type', 'application/json');

    // 요청 완료 시 실행할 콜백 함수를 설정합니다.
    xhr.onload = function() {
        if (xhr.status === 200) {
            // 응답을 JSON 형식으로 변환합니다.
            var data = JSON.parse(xhr.responseText);

            // 로딩 페이지를 숨기고 검색 결과를 표시합니다.
            document.getElementById('loadingPage').style.display = 'none';
            document.getElementById('productSection').style.display = 'block';
            renderProductList(data.products);
        } else {
            console.error('Error:', xhr.statusText);
        }
    };

    // 요청에 오류가 발생했을 때 실행할 콜백 함수를 설정합니다.
    xhr.onerror = function() {
        console.error('Request failed');
    }

    // 요청 본문을 JSON 형식으로 변환하여 요청을 보냅니다.
    xhr.send(JSON.stringify({
        searchText: searchQuery,
    }));
}

function renderProductList(products) {
    var productList = document.getElementById('productList'); 

    // 기존에 표시된 상품 리스트를 모두 제거합니다.
    while (productList.firstChild) {
        productList.removeChild(productList.firstChild);
    }

    // 상품 리스트를 브라우저에 표시합니다.
    products.slice(0, 5).forEach(function(product) {  // 상위 5개의 상품만 표시합니다.
        var productElement = document.createElement('div');
        productElement.classList.add('product');

        var productImage = document.createElement('img');
        productImage.src = product.productImage;
        productElement.appendChild(productImage);

        var productName = document.createElement('h2');
        productName.textContent = product.productName;
        productElement.appendChild(productName);

        productList.appendChild(productElement);
    });
}
