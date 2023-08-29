import { useEffect, useRef } from "react";
import useWebSocket from "react-use-websocket";
import { createChart } from "lightweight-charts";
import ThemeColors from "./ThemeColors.js";

const LightWeightChart = ({ theme, data, prediction }) => {
    const WS_URL = "ws://localhost:8000/ws/socket-server/";
    const legend = document.createElement("div");
    const chartContainerRef = useRef(null);
    const candleStickSeriesRef = useRef(null);
    const smaLineSeriesRef = useRef(null);
    const smaCount = 7;

    const { lastMessage } = useWebSocket(WS_URL, {
        onOpen: (e) => {
            console.log("socket", e.type);
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

            if (smaLineSeriesRef.current) {
                const smaData = calculateSMA([...data, modifiedPrice], smaCount);
                smaLineSeriesRef.current.setData(smaData);
            }
        }
    }, [lastMessage, data]);

    function calculateSMA(data, count) {
        var avg = function (data) {
            var sum = 0;
            for (var i = 0; i < data.length; i++) {
                sum += data[i].close;
            }
            return sum / data.length;
        };

        var result = [];
        for (var i = count - 1, len = data.length; i < len; i++) {
            var val = avg(data.slice(i - count + 1, i));
            result.push({ time: data[i].time, value: val });
        }
        return result;
    };

    useEffect(() => {
        const color = theme === "dark" ? ThemeColors.darkBlue : ThemeColors.white;
        const textColor = theme === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;

        const chart = createChart(chartContainerRef.current);

        var smaLineSeries = chart.addLineSeries({
            color: ThemeColors.smaBlue,
            lineWidth: 1,
        });

        var smaData = calculateSMA(data, smaCount);
        smaLineSeries.setData(smaData);
        smaLineSeriesRef.current = smaLineSeries;

        chart.applyOptions({
            layout: {
                background: { color },
                textColor: textColor
            },
            width: 800,
            height: 400,
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
    }, [theme, data]);

    return (
        <div className="chartContainerRef" ref={chartContainerRef}></div>
    );
};

export default LightWeightChart;