from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os


def overlay_and_plot(background_images, overlay_image, score_list):
    # Overlay 필름 이미지 on top of images
    overlay = overlay_image
    overlaid_images = []
    for background in background_images:
        background = Image.fromarray(background)
        resized_overlay = overlay.resize(background.size)
        background.paste(resized_overlay, (0, 0), resized_overlay)
        overlaid_images.append(background)

    # 옆으로 붙이기
    result = Image.new('RGB', (sum(img.width for img in overlaid_images), overlaid_images[0].height))
    x_offset = 0
    for img in overlaid_images:
        result.paste(img, (x_offset, 0))
        x_offset += img.width

    
    # plot 만들기
    fig, ax = plt.subplots(figsize=(result.width / 100, result.height / 100)) 
    x_values = np.arange(len(score_list))
    ax.plot(x_values, score_list, color='#695CFE', linewidth=35)
    ax.set_xlim(0, len(score_list) - 1)
    ax.set_ylabel('Prediction')
    ax.set_facecolor('#E4E9F7') 

    # Find the indices of the top 5 highest values
    top_5_indices = np.argsort(score_list)[-5:]

     # Plot vertical lines at the top 5 indices
    for idx in top_5_indices:
        ax.axvline(x=idx, color='#707070', linestyle='-', linewidth= 60, alpha=0.5) 


    # temporary file에 그래프 저장
    temp_plot_path = 'temp_plot.png'
    plt.savefig(temp_plot_path, bbox_inches='tight', pad_inches=0)

    # 그래프랑 concatenated image 붙이기
    plot_image = Image.open(temp_plot_path)
    plot_image = plot_image.resize((result.width, plot_image.height)) # Resize
    final_image = Image.new('RGB', (result.width, result.height + plot_image.height))
    final_image.paste(result, (0, 0))
    final_image.paste(plot_image, (0, result.height)) #그래프

    # 저장
    plt.close()

    # temporary plot file 지우기
    os.remove(temp_plot_path)

    return final_image