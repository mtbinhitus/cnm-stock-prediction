import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { AdvancedRealTimeChart, CompanyProfile, SymbolInfo, Timeline } from "react-ts-tradingview-widgets";
import Header from "../layouts/Header.js";
import Footer from "../layouts/Footer.js";
import "../styles.css";

function Homepage() {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

    useEffect(() => {
        const storedTheme = localStorage.getItem("theme");
        if (storedTheme) {
            setTheme(storedTheme);
        }
    }, []);

    const updateTheme = (newTheme) => {
        setTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    };

    const { symbol } = useParams();
    let symbol2 = symbol;

    if (symbol.slice(-4) === "USDT" || symbol.slice(-4) === "usdt") {
        symbol2 = symbol.slice(0, -1);
    }

    const styles = {
        parent: {
            display: "none"
        }
    };

    return (
        <div className="App">
            <div className="Header" id={theme}>
                <div className="Header-1">
                    <Header
                        theme={theme}
                        updateTheme={updateTheme}
                        showSearchBar={true}
                    ></Header>
                </div>
            </div>

            <div className="App-header" id={theme}>
                <div className="App-header-1">
                    <SymbolInfo
                        symbol={symbol}
                        autosize="true"
                        locale="en"
                        colorTheme={theme}
                        isTransparent="true"
                        copyrightStyles={styles}
                    ></SymbolInfo>
                </div>

                <div className="App-header-2">
                    <CompanyProfile
                        symbol={symbol2}
                        autosize="true"
                        locale="en"
                        colorTheme={theme}
                        isTransparent="true"
                        copyrightStyles={styles}
                    ></CompanyProfile>
                </div>
            </div>

            <div className="App-body" id={theme}>
                <div className="App-body-1">
                    <AdvancedRealTimeChart
                        symbol={symbol}
                        autosize="true"
                        locale="en"
                        theme={theme}
                        isTransparent="true"
                        copyrightStyles={styles}
                        interval="1"
                        range="1D"
                        timezone="Asia/Ho_Chi_Minh"
                        // eslint-disable-next-line
                        style="1"
                        details="true"
                    ></AdvancedRealTimeChart>
                </div>
            </div>

            <div className="App-footer" id={theme}>
                <div className="App-footer-1">
                    <Timeline
                        symbol={symbol2}
                        autosize="true"
                        locale="en"
                        colorTheme={theme}
                        isTransparent="true"
                        copyrightStyles={styles}
                        feedMode="symbol"
                        displayMode="compact"
                    ></Timeline>
                </div>
            </div>

            <div className="Footer" id={theme}>
                <div className="Footer-1">
                    <Footer
                        theme={theme}
                        updateTheme={updateTheme}
                    ></Footer>
                </div>
            </div>
        </div>
    );
};

export default Homepage;