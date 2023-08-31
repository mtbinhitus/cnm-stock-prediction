import { useEffect, useState } from "react";
import ChartMenu from "../components/ChartMenu.js";
import LightWeightChart from "../components/LightWeightChart.js";
import { getClosePricePredict, getKlineBTCData } from "../services/RestApi.js";
import Header from "../layouts/Header.js";
import Footer from "../layouts/Footer.js";
import "../styles.css";

function Prediction() {
    const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

    const [data, setData] = useState([]);
    const [candle, setCandle] = useState("1000");

    const [prediction, setPrediction] = useState([]);
    const [crypto, setCrypto] = useState("btcusdt");
    const [model, setModel] = useState("lstm");
    const [indicator, setIndicator] = useState(["bb"]);
    // console.log("crypto", crypto);
    // console.log("model", model);
    // console.log("indicator", indicator);

    useEffect(() => {
        getKlineBTCData(candle).then(res => {
            setData(res.sort((a, b) => a.time > b.time ? 1 : -1));
            // console.log("data", res);
        });
    }, [candle]);

    useEffect(() => {
        getClosePricePredict(crypto, model, indicator).then(res => {
            setPrediction(res);
            // console.log("prediction", res);
        });
    }, [crypto, model, indicator]);

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
        <div className="App" id={theme}>
            <div className="Header" id={theme}>
                <div className="Header-1">
                    <Header
                        theme={theme}
                        updateTheme={updateTheme}
                        showSearchBar={false}
                    ></Header>
                </div>
            </div>

            <div className="Prediction-body" id={theme}>
                <div className="Prediction-body-1" id={theme}>
                    <div className="Prediction-body-1-body" id={theme}>
                        <ChartMenu
                            theme={theme}
                            updateTheme={updateTheme}
                            candle={candle}
                            crypto={crypto}
                            model={model}
                            indicator={indicator}
                            setCandle={setCandle}
                            setCrypto={setCrypto}
                            setModel={setModel}
                            setIndicator={setIndicator}
                        ></ChartMenu>
                    </div>
                </div>

                <div className="Prediction-body-2">
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