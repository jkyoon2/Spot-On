"use client";

import "./style.css";
import ProductList from "../ProductList";
import React, { useCallback, useState, useRef } from "react";
import axios from "axios";

const server = "http://165.132.46.86:32073";

export default function Page() {
    const [loadingPageDisplay, setLoadingPageDisplay] = useState("none");
    const [searchSectionDisplay, setSearchSectionDisplay] = useState("");
    const [productSectionDisplay, setProductSectionDisplay] = useState("none");

    const [productList, setProductList] = useState([]);

    const searchInputRef = useRef<HTMLInputElement>(null);

    const onSearchButtonClick = useCallback(() => {
        setLoadingPageDisplay("block");
        setSearchSectionDisplay("none");

        const url = server + "/textSearch";
        const searchQuery = searchInputRef.current?.value;

        axios.post(
            url,
            { searchText: searchQuery },
            { headers: { "Content-Type": "application/json" } }
        ).then(res => {
            setLoadingPageDisplay("none");
            setProductSectionDisplay("block");
            setProductList(res.data.products);
        }).catch(err => {
            console.error(err);
        });
    }, []);

    return (
        <>
            <section className="hero-section">
                <div id="searchSection" className="content" style={{ display: searchSectionDisplay }}>
                    <h1>Find the item that&apos;s spot on for you</h1>
                    <div className="search-form">
                        <input
                            type="text"
                            id="searchQuery"
                            placeholder="Search for any service..."
                            ref={searchInputRef}
                            required
                        />
                        <button id="searchButton" onClick={onSearchButtonClick}>Search</button>
                    </div>
                    <div className="popular-tags">
                        Popular:
                        <ul className="tags">
                            <li><a href="#">슈퍼스타 82 ...</a></li>
                            <li><a href="#">FLOWER ZIP UP ...</a></li>
                            <li><a href="#">로고 와이드밴딩 팬츠 </a></li>
                            <li><a href="#">스퀘어 백_B ...</a></li>
                        </ul>
                    </div>
                </div>

                <div id="productSection" className="content" style={{ display: productSectionDisplay }}>
                    <h1>Top 5 Search Results</h1>
                    <ProductList productList={productList} />
                </div>

                <div id="loadingPage" className="page" style={{ display: loadingPageDisplay }}>
                    <div className="loading">
                        <div className="spinner"></div>
                    </div>
                </div>
            </section>
        </>
    );
}