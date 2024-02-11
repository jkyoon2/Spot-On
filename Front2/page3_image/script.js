const uploadBox = document.querySelector(".upload-box"),
      previewImg = uploadBox.querySelector("img"),
      fileInput = uploadBox.querySelector("input"),
      searchInput = document.getElementById("search-input"),
      searchButton = document.getElementById("search-button"),
      refreshButton = document.getElementById("refresh-button");

const loadFile = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    previewImg.src = URL.createObjectURL(file);
    previewImg.style.display = "block"; // 이미지 미리보기를 보여줌
    previewImg.addEventListener("load", () => {
        // 이미지 로드 후 검색창과 버튼들을 보여줌
        searchInput.style.display = "block";
        searchButton.style.display = "inline-block";
        refreshButton.style.display = "inline-block";
        fileInput.disabled = true; // 파일 입력 필드를 비활성화
    });
}

fileInput.addEventListener("change", loadFile);
uploadBox.addEventListener("click", () => {
    if (!fileInput.disabled) { // 파일 입력 필드가 비활성화 상태가 아닐 때만 클릭 가능
        fileInput.click();
    }
});

searchButton.addEventListener("click", function() {
    const searchTerm = searchInput.value;
    console.log("Search for:", searchTerm);
    // 검색 기능 구현
});

refreshButton.addEventListener("click", function() {
    // 페이지 새로고침 또는 입력 필드 초기화
    document.getElementById('search-input').value = ""; // 입력 필드 초기화
    window.location.reload(); // 페이지 새로고침
});
