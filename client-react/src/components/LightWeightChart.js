import { useEffect, useRef, useState } from "react";
import useWebSocket from "react-use-websocket";
import { ColorType, createChart } from "lightweight-charts";
import themeColors from "./themeColors";

const LightWeightChart = ({ theme, data }) => {
    const WS_URL = 'ws://localhost:8000/ws/socket-server/';
    // const [series, setSeries] = useState(null);
    const chartContainerRef = useRef(null);
    const seriesRef = useRef(null); // Ref to store the series

    const [priceHistory, setPriceHistory] = useState([]);
    const { lastMessage } = useWebSocket(WS_URL, {
        onOpen: (e) => {
            console.log(e.type)
        },
        shouldReconnect: (closeEvent) => true,
    });

    useEffect(() => {
        if (lastMessage !== null) {
            let price = JSON.parse(lastMessage.data);

            let price2 = {
                time: price.time / 1000,
                open: price.open,
                high: price.high,
                low: price.low,
                close: price.close,
            }

            console.log(lastMessage.data)
            if (seriesRef.current) {
                seriesRef.current.update(price2);
            }
            // series.update(price)
        }
    }, [lastMessage]);

    // const chartContainerRef = useRef();
    // const legend = document.createElement("div");

    useEffect(() => {
        const chart = createChart(chartContainerRef.current);
        setPriceHistory(data)

        const color = theme === "dark" ? themeColors.darkBlue : themeColors.white;
        const textColor = theme === "dark" ? themeColors.grayishBlue : themeColors.darkBlue;

        chart.applyOptions({
            layout: {
                background: {
                    type: ColorType.Solid,
                    color: color
                },
                textColor: textColor
            },
            width: 800,
            height: 400,
            crosshair: {
                horzLine: {
                    visible: false,
                    labelVisible: false
                }
            },
            grid: {
                vertLines: {
                    visible: false
                },
                horzLines: {
                    visible: false
                }
            },
            rightPriceScale: {
                scaleMargins: {
                    top: 0.4,
                    bottom: 0.15
                },
                borderColor: textColor
            },
            timeScale: {
                borderColor: textColor,
                timeVisible: true,
                secondsVisible: true
            }
        });

        const series = chart.addCandlestickSeries();
        series.setData(data);
        seriesRef.current = series;

        chart.timeScale().fitContent();


        // if (lastMessage !== null) {
        //     let price = JSON.parse(lastMessage.data);

        //     const lastItemTime = priceHistory[priceHistory.length - 1].time;

        //     const mappedPrice = {
        //         'time': price.time,
        //         'open': price.open,
        //         'high': price.high,
        //         'low': price.low,
        //         'close': price.close
        //     };

        //     // let temp = priceHistory.filter(kline => kline.time !== price.time);
        //     // temp.push(mappedPrice)
        //     // setPriceHistory(temp)

        //     // series.update(newCandle);
        //     // data.push(newCandle);

        //     // if (price.time > lastItemTime) {
        //     // series.update(mappedPrice);
        //     // }
        //     // else if (price.time === lastItemTime) {
        //     //     series.update(mappedPrice);
        //     // }
        // }

        return () => {
            chart.remove();
        };
    }, [theme, data]);

    return (
        <div className="chartContainerRef" ref={chartContainerRef}></div>
    );
};

export default LightWeightChart;