import { useEffect, useRef } from "react";
import useWebSocket from "react-use-websocket";
import { ColorType, createChart } from "lightweight-charts";
import themeColors from "./themeColors.js";

const LightWeightChart = ({ theme, data }) => {
    const WS_URL = "ws://localhost:8000/ws/socket-server/";
    const chartContainerRef = useRef(null);
    const seriesRef = useRef(null);

    const { lastMessage } = useWebSocket(WS_URL, {
        onOpen: (e) => {
            console.log(e.type);
        },
        shouldReconnect: (closeEvent) => {
            console.log(closeEvent.reason);
            return true;
        }
    });

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

            if (seriesRef.current) {
                seriesRef.current.update(modifiedPrice);
            }
        }
    }, [lastMessage]);

    useEffect(() => {
        const color = theme === "dark" ? themeColors.darkBlue : themeColors.white;
        const textColor = theme === "dark" ? themeColors.grayishBlue : themeColors.darkBlue;

        const chart = createChart(chartContainerRef.current);
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

        return () => {
            chart.remove();
        };
    }, [theme, data]);

    return (
        <div className="chartContainerRef" ref={chartContainerRef}></div>
    );
};

export default LightWeightChart;