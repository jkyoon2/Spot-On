const urlField = document.querySelector(".field input"),
previewArea = document.querySelector(".preview-area"),
imgTag = previewArea.querySelector(".thumbnail"),
hiddenInput = document.querySelector(".hidden-input"),
button = document.querySelector(".download-btn");

urlField.onkeyup = ()=>{
  let imgUrl = urlField.value;
  previewArea.classList.add("active");
  button.style.pointerEvents = "auto";
  if(imgUrl.indexOf("https://www.youtube.com/watch?v=") != -1){
    let vidId = imgUrl.split('v=')[1].substring(0, 11);
    let ytImgUrl = `https://img.youtube.com/vi/${vidId}/maxresdefault.jpg`;
    imgTag.src = ytImgUrl;
  }else if(imgUrl.indexOf("https://youtu.be/") != -1){
    let vidId = imgUrl.split('be/')[1].substring(0, 11);
    let ytImgUrl = `https://img.youtube.com/vi/${vidId}/maxresdefault.jpg`;
    imgTag.src = ytImgUrl;
  }else if(imgUrl.match(/\.(jpe?g|png|gif|bmp|webp)$/i)){
    imgTag.src = imgUrl;
  }else{
    imgTag.src = "";
    button.style.pointerEvents = "none";
    previewArea.classList.remove("active");
  }
  hiddenInput.value = imgTag.src;
}