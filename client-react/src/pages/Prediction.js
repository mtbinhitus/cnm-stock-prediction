import { useEffect, useState } from "react";
import LightWeightChart from "../components/LightWeightChart.js";
import Header from "../layouts/Header.js";
import Footer from "../layouts/Footer.js";
import "../styles.css";
import { getKlineBTCData } from "../services/restAPI";

function Prediction() {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState([])
    useEffect(() => {
        if (loading)
            getKlineBTCData(1000).then(res => {
                setData(res.sort((a, b) => a.time > b.time ? 1 : -1))
            }).catch(err => console.log(err));
        setLoading(false);
        console.log(data);
    }, [loading])

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
    if (loading) return <>Loading</>
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
                        data={data}
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