window.onload = function() {
    var overlayImage = document.getElementById('overlayImage');
    var timeSeriesGraph = document.getElementById('timeSeriesGraph');
    var imageContainer = document.getElementById('imageContainer');
    var findProductButton = document.getElementById('findProductButton');
    var selectedImage;

    // Assuming this is the response from the backend
    var response = {
        "overlayimage": "<overlay_image_file>",
        "time_series_graph": "<timeseries_graph>",
        "selectedMoments": [
            {
                "time": 120,
                "image": "<image1_file>"
            },
            {
                "time": 130,
                "image": "<image2_file>"
            },
            {
                "time": 140,
                "image": "<image3_file>"
            },
            {
                "time": 150,
                "image": "<image4_file>"
            },
            {
                "time": 180,
                "image": "<image5_file>"
            }
        ]
    };

    overlayImage.src = response.overlayimage;
    timeSeriesGraph.src = response.time_series_graph;

    response.selectedMoments.forEach(function(moment) {
        var img = document.createElement('img');
        img.src = moment.image;
        img.onclick = function() {
            if (selectedImage) {
                selectedImage.classList.remove('active');
            }
            img.classList.add('active');
            selectedImage = img;
            findProductButton.disabled = false;
        };
        imageContainer.appendChild(img);
    });

    findProductButton.onclick = function() {
        var selectedMoment = {
            "time": response.selectedMoments[selectedImage.dataset.index].time,
            "image": selectedImage.src
        };

        // Send selectedMoment to the backend
        // 여기에 백엔드로 데이터를 전송하는 코드를 추가하시면 됩니다.
    };
};
