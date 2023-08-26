import { useEffect, useState } from "react";
import LightWeightChart from "../components/LightWeightChart.js";
import Header from "../layouts/Header.js";
import Footer from "../layouts/Footer.js";
import "../styles.css";

function Prediction() {
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

    return (
        <div className="App">
            <div className="Header" id={theme}>
                <div className="Header-1">
                    <Header
                        theme={theme}
                        updateTheme={updateTheme}
                        showSearchBar={false}
                    ></Header>
                </div>
            </div>

            <div className="App-body" id={theme}>
                <div className="App-body-1">
                    <LightWeightChart
                        theme={theme}
                        updateTheme={updateTheme}
                    ></LightWeightChart>
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

export default Prediction;