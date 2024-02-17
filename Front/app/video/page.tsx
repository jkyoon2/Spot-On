"use client";

import "./style.css";
import ProductList from "../ProductList";
import React, { useCallback, useState, useRef, useEffect } from "react";
import axios from "axios";

const server = "http://165.132.46.86:32073";

type MomentInfo = {
    image: string
}

type Selected = React.SetStateAction<number|null>;
type SetSelected = React.Dispatch<Selected>;

function Moment(
    { image }: MomentInfo,
    idx: number,
    selected: Selected,
    setSelected: SetSelected
) {
    const onClick = () => {
        setSelected(idx);
    };

    return (
        <img
            src={server + image}
            key={image}
            alt="moment"
            style={{
                borderWidth: selected == idx ? "10px" : "0px",
                borderColor: "red",
                borderStyle: "solid"
            }}
            onClick={onClick}
        />
    )
}

function MomentList(
    { moments, selected, setSelected }: { moments: MomentInfo[], selected: Selected, setSelected: SetSelected }
) {
    return (
        <>
            {moments.map((x, i) => Moment(x, i, selected, setSelected))}
        </>
    )
}

export default function Page() {
    const linkInputRef = useRef<HTMLInputElement>(null);
    const searchInputRef = useRef<HTMLInputElement>(null);

    const [formDisplay, setFormDisplay] = useState("");
    const [momentsDisplay, setMomentsDisplay] = useState("none");
    const [productSectionDisplay, setProductSectionDisplay] = useState("none");

    const [moments, setMoments] = useState([]);
    const [selected, setSelected] = useState<number|null>(null);
    const [prompt, setPrompt] = useState("");

    const [productList, setProductList] = useState([]);

    const [vis, setVis] = useState("");

    const onFormSubmit = useCallback(() => {
        const videoUrl = linkInputRef.current?.value;
        const videoQuery = searchInputRef.current?.value;

        const url = server + "/searchMoments";

        if (!(videoUrl && videoQuery)) return;
        setPrompt(videoQuery);
        axios.post(
            url,
            {
                videoUrl: videoUrl,
                prompt: videoQuery
            },
            { headers: { "Content-Type": "application/json" } }
        ).then(res => {
            setFormDisplay("none");
            setVis(res.data.visualization);
            setMoments(res.data.selectedMoments);
            setMomentsDisplay("");
            console.log(res);
        }).catch(err => {
            console.error(err);
        });
    }, []);

    const onMomentSubmit = useCallback(() => {
        const url = server + "/videoSearch";
        if (!selected) return;
        axios.post(
            url,
            {
                selectedMoment: selected,
                prompt: prompt
            },
            { headers: { "Content-Type": "application/json" } }
        ).then(res => {
            setMomentsDisplay("none");
            setProductSectionDisplay("block");
            setProductList(res.data.products);
        }).catch(err => {
            console.error(err);
        });
    }, [selected]);

    return (
        <>
            <div className="form" style={{ display: formDisplay }}>
                <header>Find Item in the Video</header>
                <div className="url-input">
                <span className="title">Paste video url:</span>
                <div className="field">
                    <input
                        type="text"
                        placeholder="https://www.youtube.com/watch?v=lqwdD2ivIbM"
                        ref={linkInputRef}
                        required
                    />
                    <span className="bottom-line"></span>
                </div>
                </div>
                <div className="url-input">
                <span className="title">Enter the item you are looking for in the video:</span>
                <div className="field">
                    <input
                        type="text"
                        placeholder="Type here..."
                        name="searchTerm"
                        ref={searchInputRef}
                    />
                    <span className="bottom-line"></span>
                </div>
                </div>
                <button
                    className="download-btn"
                    name="button"
                    onClick={onFormSubmit}
                >Search</button>
            </div>
            <div style={{ display: momentsDisplay }}>
                <img src={vis} alt="visualization"/>
                <MomentList moments={moments} selected={selected} setSelected={setSelected} />
                <button
                    onClick={onMomentSubmit}
                >Submit</button>
            </div>
            <div id="productSection" className="content" style={{ display: productSectionDisplay }}>
                <h1>Top 5 Search Results</h1>
                <ProductList productList={productList} />
            </div>
        </>
    );
}