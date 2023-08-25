import { useEffect, useState } from "react";
import LightChart from "../components/LightChart.js";
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

            <div>
                <LightChart
                    theme={theme}
                    updateTheme={updateTheme}
                ></LightChart>
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