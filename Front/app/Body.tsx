"use client"

import { useCallback, useState, ReactNode } from "react";
import Image from "next/image";

export default function Body({ children }: { children: ReactNode }) {
    const [bodyStyle, setBodyStyle] = useState("");
    const [sideBarState, setSideBarState] = useState("close");
    const [modeText, setModeText] = useState("Dark Mode");

    const onToggleClick = useCallback(() => {
        if (sideBarState === "") {
            setSideBarState("close");
        } else {
            setSideBarState("");
        }
    }, [sideBarState]);

    const onSearchBtnClick = useCallback(() => {
        setSideBarState("");
    }, []);

    const onModeSwitchClick = useCallback(() => {
        if (bodyStyle !== "dark") {
            setBodyStyle("dark");
            setModeText("Light mode");
        } else {
            setBodyStyle("");
            setModeText("Dark mode");
        }
    }, [bodyStyle]);

    return (
        <body className={bodyStyle}>
            <nav className={"sidebar " + sideBarState}>
                <header>
                    <div className="image-text">
                        <span className="image">
                            <Image src="/logo.png" width={40} height={40} alt="logo" />
                        </span>

                        <div className="text logo-text">
                            <span className="name">Spot On</span>
                            <span className="profession">Search Engine</span>
                        </div>
                    </div>

                    <i className='bx bx-chevron-right toggle' onClick={onToggleClick}></i>
                </header>

                <div className="menu-bar">

                    <div className="menu">

                        <li className="search-box" onClick={onSearchBtnClick}>
                            <i className='bx bx-search icon'></i>
                            <input type="text" placeholder="Search..." />
                        </li>

                        <ul className="menu-links">
                            <li className="nav-link">
                                <a href="/">
                                    <i className='bx bx-home-alt icon' ></i>
                                    <span className="text nav-text">Home</span>
                                </a>
                            </li>

                            <li className="nav-link">
                                <a href="/text">
                                    <i className="bx bx-pencil icon" ></i>
                                    <span className="text nav-text">Text</span>
                                </a>
                            </li>

                            <li className="nav-link">
                                <a href="/image">
                                    <i className='bx bx-image icon'></i>
                                    <span className="text nav-text">Image</span>
                                </a>
                            </li>

                            <li className="nav-link">
                                <a href="/video">
                                    <i className='bx bx-video icon' ></i>
                                    <span className="text nav-text">Video</span>
                                </a>
                            </li>
                        </ul>
                    </div>

                    <div className="bottom-content">
                        <li className="">
                            <a href="#">
                                <i className='bx bx-log-out icon' ></i>
                                <span className="text nav-text">Logout</span>
                            </a>
                        </li>

                        <li className="mode">
                            <div className="sun-moon">
                                <i className='bx bx-moon icon moon'></i>
                                <i className='bx bx-sun icon sun'></i>
                            </div>
                            <span className="mode-text text">{modeText}</span>

                            <div className="toggle-switch" onClick={onModeSwitchClick}>
                                <span className="switch"></span>
                            </div>
                        </li>
                    </div>
                </div>
            </nav>

            <section className="home">
                <div className="text">Spot On</div>
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

            {children}
        </body>
    )
}