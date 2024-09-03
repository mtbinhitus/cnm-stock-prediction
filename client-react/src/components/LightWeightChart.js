import { useEffect, useRef, useState } from "react";
import useWebSocket from "react-use-websocket";
import { createChart } from "lightweight-charts";
import ThemeColors from "./ThemeColors.js";
import { getClosePricePredict } from "../services/RestApi.js";

const LightWeightChart = ({ theme, smaCount, data, prediction, crypto, model, indicator }) => {
    const WS_URL = process.env.REACT_APP_WS_URL;
    const chartContainerRef = useRef(null);
    const chartRef = useRef(null);
    const legendRef = useRef(null);
    const themeRef = useRef(theme);
    const candleStickSeriesRef = useRef(null);
    const sma5LineSeriesRef = useRef(null);
    const sma10LineSeriesRef = useRef(null);
    const sma20LineSeriesRef = useRef(null);
    const sma40LineSeriesRef = useRef(null);
    const predictionLineSeriesRef = useRef(null);
    const [prevPredict, setPrevPredict] = useState(null);

    const [newData, setNewData] = useState([]);
    useEffect(() => {
        if (data.length !== 0) {
            setNewData([...data]);
        }
    }, [data]);

    const { lastMessage } = useWebSocket(WS_URL, {
        onOpen: (event) => {
            console.log("socket", event.type);
        },
        shouldReconnect: () => {
            return true;
        }
    });

    function calculateSMA(data, count) {
        const avg = function (data) {
            let sum = 0;
            for (let i = 0; i < data.length; i++) {
                sum += data[i].close;
            }
            return sum / data.length;
        };

        const result = [];
        for (let i = count - 1; i < data.length; i++) {
            const val = avg(data.slice(i - count + 1, i + 1));
            result.push({ time: data[i].time, value: val });
        }
        return result;
    };

    const setTooltipHtml = (name, time, open, high, low, close) => {
        if (close - open >= 0) {
            legendRef.current.innerHTML = `
                <div style="font-size: 24px; margin: 4px 0px;">${name}</div>
                <div style="font-size: 20px; margin: 4px 0px;">
                    <span>Open</span>
                    <span style="color: ${ThemeColors.candlePositive};">${open}</span>
                    <span>High</span>
                    <span style="color: ${ThemeColors.candlePositive};">${high}</span>
                </div>
                <div style="font-size: 20px; margin: 4px 0px;">
                    <span>Low</span>
                    <span style="color: ${ThemeColors.candlePositive};">${low}</span>
                    <span>Close</span>
                    <span style="color: ${ThemeColors.candlePositive};">${close}</span>
                </div>
                <div style="font-size: 16px; margin: 4px 0px;">${time}</div>
            `;
        } else {
            legendRef.current.innerHTML = `
                <div style="font-size: 24px; margin: 4px 0px;">${name}</div>
                <div style="font-size: 20px; margin: 4px 0px;">
                    <span>Open</span>
                    <span style="color: ${ThemeColors.candleNegative};">${open}</span>
                    <span>High</span>
                    <span style="color: ${ThemeColors.candleNegative};">${high}</span>
                </div>
                <div style="font-size: 20px; margin: 4px 0px;">
                    <span>Low</span>
                    <span style="color: ${ThemeColors.candleNegative};">${low}</span>
                    <span>Close</span>
                    <span style="color: ${ThemeColors.candleNegative};">${close}</span>
                </div>
                <div style="font-size: 16px; margin: 4px 0px;">${time}</div>
            `;
        }
    };

    useEffect(() => {
        const color = themeRef.current === "dark" ? ThemeColors.darkBlue : ThemeColors.white;
        const textColor = themeRef.current === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;

        chartRef.current = createChart(chartContainerRef.current);
        chartRef.current.applyOptions({
            width: 1178,
            height: 500,
            layout: {
                background: { color },
                textColor: textColor
            },
            crosshair: {
                horzLine: {
                    visible: false,
                    labelVisible: false
                },
                vertLine: {
                    visible: true,
                    labelVisible: false
                }
            },
            grid: {
                horzLines: {
                    visible: false
                },
                vertLines: {
                    visible: false
                }
            },
            rightPriceScale: {
                scaleMargins: {
                    top: 0.4,
                    bottom: 0.2
                },
                borderColor: textColor
            },
            timeScale: {
                borderColor: textColor,
                timeVisible: true
            }
        });

        candleStickSeriesRef.current = chartRef.current.addCandlestickSeries({
            title: "Current price"
        });

        predictionLineSeriesRef.current = chartRef.current.addLineSeries({
            title: "Predicted price",
            color: ThemeColors.predictionColor,
            lineWidth: 1
        });

        legendRef.current = document.createElement("div");
        legendRef.current.className = "legend";
        legendRef.current.style = `position: absolute; left: 0px; top: 0px; z-index: 1;`;
        legendRef.current.style.color = textColor;
        chartContainerRef.current.appendChild(legendRef.current);

        return () => {
            legendRef.current.remove();
            chartRef.current.remove();
        };
    }, []);

    useEffect(() => {
        candleStickSeriesRef.current.setData([]);
    }, [data]);

    useEffect(() => {
        if (data.some(item => item.time !== undefined)) {
            candleStickSeriesRef.current.setData(data);
        }
    }, [data]);

    useEffect(() => {
        if (prediction && prediction.time !== undefined) {
            const modifiedPrediction = {
                time: prediction.time,
                value: prediction.value
            };

            if (prevPredict !== null && prevPredict[prevPredict.length - 1].time > prediction.time) {
                predictionLineSeriesRef.current.setData(prevPredict);
            } else {
                setPrevPredict([modifiedPrediction]);
                predictionLineSeriesRef.current.setData([modifiedPrediction]);
            }
        }
        // eslint-disable-next-line
    }, [prediction]);

    useEffect(() => {
        if (sma5LineSeriesRef.current) {
            chartRef.current.removeSeries(sma5LineSeriesRef.current);
            sma5LineSeriesRef.current = null;
        }

        if (sma10LineSeriesRef.current) {
            chartRef.current.removeSeries(sma10LineSeriesRef.current);
            sma10LineSeriesRef.current = null;
        }

        if (sma20LineSeriesRef.current) {
            chartRef.current.removeSeries(sma20LineSeriesRef.current);
            sma20LineSeriesRef.current = null;
        }

        if (sma40LineSeriesRef.current) {
            chartRef.current.removeSeries(sma40LineSeriesRef.current);
            sma40LineSeriesRef.current = null;
        }
    }, [data]);

    useEffect(() => {
        const color = theme === "dark" ? ThemeColors.darkBlue : ThemeColors.white;
        const textColor = theme === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;

        chartRef.current.applyOptions({
            width: 1178,
            height: 500,
            layout: {
                background: { color },
                textColor: textColor
            },
            crosshair: {
                horzLine: {
                    visible: false,
                    labelVisible: false
                },
                vertLine: {
                    visible: true,
                    labelVisible: false
                }
            },
            grid: {
                horzLines: {
                    visible: false
                },
                vertLines: {
                    visible: false
                }
            },
            rightPriceScale: {
                scaleMargins: {
                    top: 0.4,
                    bottom: 0.2
                },
                borderColor: textColor
            },
            timeScale: {
                borderColor: textColor,
                timeVisible: true
            }
        });

        legendRef.current.style.color = textColor;
    }, [theme]);

    useEffect(() => {
        const lastIndex = candleStickSeriesRef.current.dataByIndex(newData.length - 1);
        if (lastIndex) {
            const updateLegend = param => {
                const validCrosshairPoint = !(
                    param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0
                );

                const bar = validCrosshairPoint ? param.seriesData.get(candleStickSeriesRef.current) : lastIndex;

                if (bar !== undefined) {
                    const time = new Date(0);
                    time.setUTCSeconds(bar.time);
                    const day = time.getUTCDate();
                    const month = time.toLocaleString("default", { month: "long" });
                    const year = time.getUTCFullYear();
                    const hours = time.getUTCHours().toString().padStart(2, "0");
                    const minutes = time.getUTCMinutes().toString().padStart(2, "0");

                    const open = bar.open.toFixed(2);
                    const high = bar.high.toFixed(2);
                    const low = bar.low.toFixed(2);
                    const close = bar.close.toFixed(2);

                    const symbolName = "BINANCE:BTCUSDT";
                    const formattedTime = `${day} ${month} ${year} ${hours}:${minutes}`;

                    setTooltipHtml(symbolName, formattedTime, open, high, low, close);
                }
            };

            chartRef.current.subscribeCrosshairMove(updateLegend);
            updateLegend(undefined);
        }
    }, [newData]);

    useEffect(() => {
        function manageSMA(chartRef, seriesRef, data, period, color) {
            if (smaCount.includes(period)) {
                if (!seriesRef.current) {
                    seriesRef.current = chartRef.current.addLineSeries({
                        title: "SMA " + period + "",
                        color: color,
                        lineWidth: 1
                    });

                    const smaData = calculateSMA(data.slice(0, data.length - 1), period);
                    if (data.some(item => item.time !== undefined)) {
                        seriesRef.current.setData(smaData);
                    }
                }
            } else {
                if (seriesRef.current) {
                    chartRef.current.removeSeries(seriesRef.current);
                    seriesRef.current = null;
                }
            }
        }

        manageSMA(chartRef, sma5LineSeriesRef, data, "5", ThemeColors.sma5Color);
        manageSMA(chartRef, sma10LineSeriesRef, data, "10", ThemeColors.sma10Color);
        manageSMA(chartRef, sma20LineSeriesRef, data, "20", ThemeColors.sma20Color);
        manageSMA(chartRef, sma40LineSeriesRef, data, "40", ThemeColors.sma40Color);
    }, [data, smaCount]);

    useEffect(() => {
        if (lastMessage !== null) {
            let price = JSON.parse(lastMessage.data);
            let priceTimeMillis = price.time;
            let priceTimeUTC = new Date(priceTimeMillis);
            priceTimeUTC.setHours(priceTimeUTC.getHours() + 7);

            let modifiedPrice = {
                time: priceTimeUTC.getTime() / 1000,
                open: price.open,
                high: price.high,
                low: price.low,
                close: price.close
            };

            if (newData.length !== 0 && modifiedPrice.time === newData[newData.length - 1].time) {
                newData[newData.length - 1] = modifiedPrice;
            }

            if (newData.length !== 0 && modifiedPrice.time > newData[newData.length - 1].time) {
                setNewData([...newData, modifiedPrice]);
            }

            if (candleStickSeriesRef.current) {
                candleStickSeriesRef.current.update(modifiedPrice);
            }

            if (predictionLineSeriesRef.current && prevPredict) {
                if (modifiedPrice.time > prevPredict[prevPredict.length - 1].time) {
                    getClosePricePredict(crypto, model, indicator).then(res => {
                        setPrevPredict([...prevPredict, res]);
                        if (res.time !== undefined) {
                            predictionLineSeriesRef.current.update(res);
                        }
                    });
                }
            }

            if (smaCount.includes("5") && sma5LineSeriesRef.current) {
                const smaData = calculateSMA(newData.slice(-5), 5);
                sma5LineSeriesRef.current.update(smaData[0]);
            }

            if (smaCount.includes("10") && sma10LineSeriesRef.current) {
                const smaData = calculateSMA(newData.slice(-10), 10);
                sma10LineSeriesRef.current.update(smaData[0]);
            }

            if (smaCount.includes("20") && sma20LineSeriesRef.current) {
                const smaData = calculateSMA(newData.slice(-20), 20);
                sma20LineSeriesRef.current.update(smaData[0]);
            }

            if (smaCount.includes("40") && sma40LineSeriesRef.current) {
                const smaData = calculateSMA(newData.slice(-40), 40);
                sma40LineSeriesRef.current.update(smaData[0]);
            }
        }
        // eslint-disable-next-line
    }, [lastMessage, newData, smaCount]);

    return (
        <div className="chartContainerRef" style={{ position: "relative" }} ref={chartContainerRef}></div>
    );
};

export default LightWeightChart;