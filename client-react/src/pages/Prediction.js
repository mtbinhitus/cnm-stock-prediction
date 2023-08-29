import { useEffect, useState } from "react";
import LightWeightChart from "../components/LightWeightChart.js";
import { getKlineBTCData } from "../services/restAPI.js";
import { getClosePricePredict } from "../services/restAPI.js";
import Header from "../layouts/Header.js";
import Footer from "../layouts/Footer.js";
import "../styles.css";

function Prediction() {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");
    const [data, setData] = useState([]);
    const [prediction, setPrediction] = useState([]);

    useEffect(() => {
        const limit = 1000;
        getKlineBTCData(limit).then(res => {
            setData(res.sort((a, b) => a.time > b.time ? 1 : -1));
            console.log("data", res);
        });
    }, []);


    useEffect(() => {
        const sticker = "BTCUSDT";
        const model = "LSTM";
        const indicator = ["Close", "POC", "MA"];

        getClosePricePredict(sticker, model, indicator).then(res => {
            setPrediction(res);
            console.log("prediction", res);
        });
    }, []);

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
                        data={data}
                        prediction={prediction}
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