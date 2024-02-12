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
    document.getElementById('loadingPage').style.display = 'flex'; 
    
    // 이미지 로딩을 시뮬레이션하기 위해 setTimeout 사용
    setTimeout(function() {
        document.getElementById('loadingPage').style.display = 'none';
        // 여기서 'imageResults' 요소가 실제로 존재하고 이를 표시하려고 한다고 가정합니다.
        // 'imageResults' 요소가 없으면 이 부분을 적절히 수정하거나 해당 요소를 HTML에 추가해야 합니다.
        var imageResults = document.getElementById('imageResults');
        if (imageResults) {
            imageResults.style.display = 'block';
        }
    }, 10000); // 10초 동안 로딩 페이지 표시
}

