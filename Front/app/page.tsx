"use client";

import React, { useRef } from "react";
import "./style.css";

export default function Home() {
    const imageListRef = useRef<HTMLUListElement>(null);
    const sliderWrapperRef = useRef<HTMLDivElement>(null);
    const slideButtonRef = useRef<HTMLButtonElement>(null);
    const sliderScrollbarRef = useRef<HTMLDivElement>(null);
    const scrollbarThumbRef = useRef<HTMLDivElement>(null);

    const initSlider = () => {
        const imageList = imageListRef.current;
        const slideButtons = [sliderWrapperRef.current, slideButtonRef.current];
        const sliderScrollbar = sliderScrollbarRef.current;
        const scrollbarThumb = scrollbarThumbRef.current;

        if (!(imageList && slideButtons.reduce((x, y) => x && y) && sliderScrollbar && scrollbarThumb)) return;

        const maxScrollLeft = imageList.scrollWidth - imageList.clientWidth;

        // Handle scrollbar thumb drag
        scrollbarThumb.addEventListener("mousedown", (e) => {
            const startX = e.clientX;
            const thumbPosition = scrollbarThumb.offsetLeft;
            const maxThumbPosition = sliderScrollbar.getBoundingClientRect().width - scrollbarThumb.offsetWidth;

            // Update thumb position on mouse move
            const handleMouseMove = (e: any) => {
                const deltaX = e.clientX - startX;
                const newThumbPosition = thumbPosition + deltaX;

                // Ensure the scrollbar thumb stays within bounds
                const boundedPosition = Math.max(0, Math.min(maxThumbPosition, newThumbPosition));
                const scrollPosition = (boundedPosition / maxThumbPosition) * maxScrollLeft;

                scrollbarThumb.style.left = `${boundedPosition}px`;
                imageList.scrollLeft = scrollPosition;
            }

            // Remove event listeners on mouse up
            const handleMouseUp = () => {
                document.removeEventListener("mousemove", handleMouseMove);
                document.removeEventListener("mouseup", handleMouseUp);
            }

            // Add event listeners for drag interaction
            document.addEventListener("mousemove", handleMouseMove);
            document.addEventListener("mouseup", handleMouseUp);
        });

        // Slide images according to the slide button clicks
        slideButtons.forEach(button => {
            button?.addEventListener("click", () => {
                const direction = button.id === "prev-slide" ? -1 : 1;
                const scrollAmount = imageList.clientWidth * direction;
                imageList.scrollBy({ left: scrollAmount, behavior: "smooth" });
            });
        });

         // Show or hide slide buttons based on scroll position
        const handleSlideButtons = () => {
            if (!(slideButtons[0] && slideButtons[1])) return;
            slideButtons[0].style.display = imageList.scrollLeft <= 0 ? "none" : "flex";
            slideButtons[1].style.display = imageList.scrollLeft >= maxScrollLeft ? "none" : "flex";
        }

        // Update scrollbar thumb position based on image scroll
        const updateScrollThumbPosition = () => {
            const scrollPosition = imageList.scrollLeft;
            const thumbPosition = (scrollPosition / maxScrollLeft) * (sliderScrollbar.clientWidth - scrollbarThumb.offsetWidth);
            scrollbarThumb.style.left = `${thumbPosition}px`;
        }

        // Call these two functions when image list scrolls
        imageList.addEventListener("scroll", () => {
            updateScrollThumbPosition();
            handleSlideButtons();
        });
    };

    window.addEventListener("resize", initSlider);
    window.addEventListener("load", initSlider);

    return (
        <>
            <section className="home">
                <div className="text">Spot On</div>
            </section>

            <section className="home3">
                <p className="spot-on">Spot On</p>
                <p className="description">텍스트, 이미지, 비디오로 당신이 찾고자 하는 것을 찾아드립니다</p>
            </section>

            <section className="header-bar">
                <nav className="navbar">
                    <ul className="menu-links">
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Basket</a></li>
                        <li><a href="#">My Page</a></li>
                        <li><a href="#">Sign In</a></li>
                        <li className="join-btn"><a href="#">Join Us</a></li>
                    </ul>
                </nav>
            </section>

            <section className="image-slider">
                <div className="container">
                    <div className="slider-wrapper" ref={sliderWrapperRef}>
                    <button id="prev-slide" className="slide-button material-symbols-rounded" ref={slideButtonRef}>
                    </button>
                    <ul className="image-list" ref={imageListRef}>
                        <img className="image-item" src="/images/img-1.jpg" alt="img-1" />
                        <img className="image-item" src="/images/img-2.jpg" alt="img-2" />
                        <img className="image-item" src="/images/img-3.jpg" alt="img-3" />
                        <img className="image-item" src="/images/img-4.jpg" alt="img-4" />
                        <img className="image-item" src="/images/img-5.jpg" alt="img-5" />
                        <img className="image-item" src="/images/img-6.jpg" alt="img-6" />
                        <img className="image-item" src="/images/img-7.jpg" alt="img-7" />
                        <img className="image-item" src="/images/img-8.jpg" alt="img-8" />
                        <img className="image-item" src="/images/img-9.jpg" alt="img-9" />
                        <img className="image-item" src="/images/img-10.jpg" alt="img-10" />
                    </ul>
                    <button id="next-slide" className="slide-button material-symbols-rounded bx bx-chevron-right" />
                    </div>
                    <div className="slider-scrollbar" ref={sliderScrollbarRef}>
                    <div className="scrollbar-track">
                        <div className="scrollbar-thumb" ref={scrollbarThumbRef}></div>
                    </div>
                    </div>
                </div>
            </section>
        </>
    );
}
