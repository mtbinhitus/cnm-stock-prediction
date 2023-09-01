import { useEffect, useRef } from "react";
import useWebSocket from "react-use-websocket";
import { createChart } from "lightweight-charts";
import ThemeColors from "./ThemeColors.js";

const LightWeightChart = ({ theme, smaCount, data, prediction }) => {
    const WS_URL = "ws://localhost:8000/ws/socket-server/";
    const legend = document.createElement("div");
    const chartContainerRef = useRef(null);
    const candleStickSeriesRef = useRef(null);
    const sma5LineSeriesRef = useRef(null);
    const sma10LineSeriesRef = useRef(null);
    const sma20LineSeriesRef = useRef(null);
    const sma40LineSeriesRef = useRef(null);

    const { lastMessage } = useWebSocket(WS_URL, {
        onOpen: (event) => {
            console.log("socket", event.type);
        },
        shouldReconnect: () => {
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

            if (candleStickSeriesRef.current) {
                candleStickSeriesRef.current.update(modifiedPrice);
            }

            if (smaCount.includes("5") && sma5LineSeriesRef.current) {
                const smaData = calculateSMA([...data, modifiedPrice], "5");
                sma5LineSeriesRef.current.setData(smaData);
            }

            if (smaCount.includes("10") && sma10LineSeriesRef.current) {
                const smaData = calculateSMA([...data, modifiedPrice], "10");
                sma10LineSeriesRef.current.setData(smaData);
            }

            if (smaCount.includes("20") && sma20LineSeriesRef.current) {
                const smaData = calculateSMA([...data, modifiedPrice], "20");
                sma20LineSeriesRef.current.setData(smaData);
            }

            if (smaCount.includes("40") && sma40LineSeriesRef.current) {
                const smaData = calculateSMA([...data, modifiedPrice], "40");
                sma40LineSeriesRef.current.setData(smaData);
            }
        }
    }, [lastMessage, data, smaCount]);

    function calculateSMA(data, count) {
        if (count === 0) {
            return [];
        }

        const avg = function (data) {
            let sum = 0;
            for (let i = 0; i < data.length; i++) {
                sum += data[i].close;
            }
            return sum / data.length;
        };

        const result = [];
        for (let i = count - 1, len = data.length; i < len; i++) {
            const val = avg(data.slice(i - count + 1, i));
            result.push({ time: data[i].time, value: val });
        }
        return result;
    };

    useEffect(() => {
        const color = theme === "dark" ? ThemeColors.darkBlue : ThemeColors.white;
        const textColor = theme === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;

        const chart = createChart(chartContainerRef.current);

        if (smaCount.includes("5")) {
            const sma5LineSeries = chart.addLineSeries({
                color: ThemeColors.sma5Color,
                lineWidth: 1
            });

            const smaData = calculateSMA(data, "5");
            sma5LineSeries.setData(smaData);
        }

        if (smaCount.includes("10")) {
            const sma10LineSeries = chart.addLineSeries({
                color: ThemeColors.sma10Color,
                lineWidth: 1
            });

            const smaData = calculateSMA(data, "10");
            sma10LineSeries.setData(smaData);
        }

        if (smaCount.includes("20")) {
            const sma20LineSeries = chart.addLineSeries({
                color: ThemeColors.sma20Color,
                lineWidth: 1
            });

            const smaData = calculateSMA(data, "20");
            sma20LineSeries.setData(smaData);
        }

        if (smaCount.includes("40")) {
            const sma40LineSeries = chart.addLineSeries({
                color: ThemeColors.sma40Color,
                lineWidth: 1
            });

            const smaData = calculateSMA(data, "40");
            sma40LineSeries.setData(smaData);
        }

        chart.applyOptions({
            layout: {
                background: { color },
                textColor: textColor
            },
            width: 1000,
            height: 500,
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
                    bottom: 0.2
                },
                borderColor: textColor
            },
            timeScale: {
                borderColor: textColor,
                timeVisible: true,
                secondsVisible: true
            }
        });

        const candleStickSeries = chart.addCandlestickSeries();
        candleStickSeries.setData(data);
        candleStickSeriesRef.current = candleStickSeries;

        const symbolName = "BINANCE:BTCUSDT";
        legend.style = `position: absolute; left: 12px; top: 12px; z-index: 1; font-size: 14px; line-height: 18px; font-weight: 300;`;
        legend.style.color = textColor;
        chartContainerRef.current.appendChild(legend);

        const setTooltipHtml = (name, time, open, high, low, close) => {
            if (close - open >= 0) {
                legend.innerHTML = `
                    <div style="font-size: 20px; margin: 4px 0px;">${name}</div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Open</span>
                        <span style="color: ${ThemeColors.candlePositive};">${open}</span>
                        <span>High</span>
                        <span style="color: ${ThemeColors.candlePositive};">${high}</span>
                    </div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Low</span>
                        <span style="color: ${ThemeColors.candlePositive};">${low}</span>
                        <span>Close</span>
                        <span style="color: ${ThemeColors.candlePositive};">${close}</span>
                    </div>
                    <div style="font-size: 12px; margin: 4px 0px;">${time}</div>
                `;
            } else {
                legend.innerHTML = `
                    <div style="font-size: 20px; margin: 4px 0px;">${name}</div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Open</span>
                        <span style="color: ${ThemeColors.candleNegative};">${open}</span>
                        <span>High</span>
                        <span style="color: ${ThemeColors.candleNegative};">${high}</span>
                    </div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Low</span>
                        <span style="color: ${ThemeColors.candleNegative};">${low}</span>
                        <span>Close</span>
                        <span style="color: ${ThemeColors.candleNegative};">${close}</span>
                    </div>
                    <div style="font-size: 12px; margin: 4px 0px;">${time}</div>
                `;
            }
        };

        const lastIndex = candleStickSeries.dataByIndex(data.length - 1);

        if (lastIndex) {
            const updateLegend = param => {
                const validCrosshairPoint = !(
                    param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0
                );

                const bar = validCrosshairPoint ? param.seriesData.get(candleStickSeries) : lastIndex;

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

                const formattedTime = `${day} ${month} ${year} ${hours}:${minutes}`;

                setTooltipHtml(symbolName, formattedTime, open, high, low, close);
            };

            chart.subscribeCrosshairMove(updateLegend);
            updateLegend(undefined);
        }

        return () => {
            chart.remove();
        };
        // eslint-disable-next-line
    }, [theme, data, smaCount]);

    return (
        <div style={{ position: "relative" }} ref={chartContainerRef}></div>
    );
};

export default LightWeightChart;