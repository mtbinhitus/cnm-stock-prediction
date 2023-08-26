import { useEffect, useRef } from "react";
import { ColorType, createChart } from "lightweight-charts";
import themeColors from "./themeColors";

const LightWeightChart = ({ theme }) => {
    const chartContainerRef = useRef();
    const legend = document.createElement("div");

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
                borderColor: textColor
            }
        });

        const candleSeries = chart.addCandlestickSeries();
        const data = [
            { time: "2018-12-22", open: 75.16, high: 82.84, low: 36.16, close: 45.72 },
            { time: "2018-12-23", open: 45.12, high: 53.90, low: 45.12, close: 48.09 },
            { time: "2018-12-24", open: 60.71, high: 60.71, low: 53.39, close: 59.29 },
            { time: "2018-12-25", open: 68.26, high: 68.26, low: 59.04, close: 60.50 },
            { time: "2018-12-26", open: 67.71, high: 105.85, low: 66.67, close: 91.04 },
            { time: "2018-12-27", open: 91.04, high: 121.40, low: 82.70, close: 111.40 },
            { time: "2018-12-28", open: 111.51, high: 142.83, low: 103.34, close: 131.25 },
            { time: "2018-12-29", open: 131.33, high: 151.17, low: 77.68, close: 96.43 },
            { time: "2018-12-30", open: 106.33, high: 110.20, low: 90.39, close: 98.10 },
            { time: "2018-12-31", open: 109.87, high: 114.69, low: 85.66, close: 111.26 }
        ];

        candleSeries.setData(data);

        let lastClose = data[data.length - 1].close;
        let lastIndex = data.length - 1;
        let targetIndex = lastIndex + 105 + Math.round(Math.random() + 30);
        let targetPrice = getRandomPrice();
        let currentIndex = lastIndex + 1;
        let currentBusinessDay = { day: 29, month: 5, year: 2019 };
        let ticksInCurrentBar = 0;
        let currentBar = {
            open: null,
            high: null,
            low: null,
            close: null,
            time: currentBusinessDay
        };

        function mergeTickToBar(price) {
            if (currentBar.open === null) {
                currentBar.open = price;
                currentBar.high = price;
                currentBar.low = price;
                currentBar.close = price;
            } else {
                currentBar.close = price;
                currentBar.high = Math.max(currentBar.high, price);
                currentBar.low = Math.min(currentBar.low, price);
            }
            candleSeries.update(currentBar);
        };

        function reset() {
            candleSeries.setData(data);
            lastClose = data[data.length - 1].close;
            lastIndex = data.length - 1;
            targetIndex = lastIndex + 5 + Math.round(Math.random() + 30);
            targetPrice = getRandomPrice();
            currentIndex = lastIndex + 1;
            currentBusinessDay = { day: 29, month: 5, year: 2019 };
            ticksInCurrentBar = 0;
        };

        function getRandomPrice() {
            return 10 + Math.round(Math.random() * 10000) / 100;
        };

        function nextBusinessDay(time) {
            const d = new Date();
            d.setUTCFullYear(time.year);
            d.setUTCMonth(time.month - 1);
            d.setUTCDate(time.day + 1);
            d.setUTCHours(0, 0, 0, 0);

            return {
                year: d.getUTCFullYear(),
                month: d.getUTCMonth() + 1,
                day: d.getUTCDate()
            };
        };

        const interval = setInterval(() => {
            const deltaY = targetPrice - lastClose;
            const deltaX = targetIndex - lastIndex;
            const angle = deltaY / deltaX;
            const basePrice = lastClose + (currentIndex - lastIndex) * angle;
            const noise = 0.1 - Math.random() * 0.1 + 1.0;
            const noisedPrice = basePrice * noise;
            mergeTickToBar(noisedPrice);

            if (++ticksInCurrentBar === 5) {
                currentIndex++;
                currentBusinessDay = nextBusinessDay(currentBusinessDay);
                currentBar = {
                    open: null,
                    high: null,
                    low: null,
                    close: null,
                    time: currentBusinessDay
                };

                ticksInCurrentBar = 0;
                if (currentIndex === 5000) {
                    reset();
                    return;
                }

                if (currentIndex === targetIndex) {
                    lastClose = noisedPrice;
                    lastIndex = currentIndex;
                    targetIndex = lastIndex + 5 + Math.round(Math.random() + 30);
                    targetPrice = getRandomPrice();
                }
            }
        }, 200);

        const symbolName = "BINANCE:BTCUSDT";
        legend.style = `position: absolute; left: 12px; top: 12px; z-index: 1; font-size: 14px; line-height: 18px; font-weight: 300;`;
        legend.style.color = textColor;
        chartContainerRef.current.appendChild(legend);

        const getLastBar = series => {
            const lastIndex = series.dataByIndex(Math.Infinity, -1);
            return series.dataByIndex(lastIndex);
        };

        const formatOpen = open => open.toFixed(2);
        const formatHigh = high => high.toFixed(2);
        const formatLow = low => low.toFixed(2);
        const formatClose = close => close.toFixed(2);

        const setTooltipHtml = (name, date, open, high, low, close) => {
            if (close - open > 0) {
                legend.innerHTML = `
                    <div style="font-size: 20px; margin: 4px 0px;">${name}</div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Open</span>
                        <span style="color: ${themeColors.candlePositive};">${open}</span>
                        <span>High</span>
                        <span style="color: ${themeColors.candlePositive};">${high}</span>
                    </div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Low</span>
                        <span style="color: ${themeColors.candlePositive};">${low}</span>
                        <span>Close</span>
                        <span style="color: ${themeColors.candlePositive};">${close}</span>
                    </div>
                    <div style="font-size: 12px; margin: 4px 0px;">${date}</div>
                `;
            } else {
                legend.innerHTML = `
                    <div style="font-size: 20px; margin: 4px 0px;">${name}</div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Open</span>
                        <span style="color: ${themeColors.candleNegative};">${open}</span>
                        <span>High</span>
                        <span style="color: ${themeColors.candleNegative};">${high}</span>
                    </div>
                    <div style="font-size: 16px; margin: 4px 0px;">
                        <span>Low</span>
                        <span style="color: ${themeColors.candleNegative};">${low}</span>
                        <span>Close</span>
                        <span style="color: ${themeColors.candleNegative};">${close}</span>
                    </div>
                    <div style="font-size: 12px; margin: 4px 0px;">${date}</div>
                `;
            }
        };

        const updateLegend = param => {
            const validCrosshairPoint = !(
                param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0
            );

            const bar = validCrosshairPoint ? param.seriesData.get(candleSeries) : getLastBar(candleSeries);
            const time = bar.time;
            const open = bar.open;
            const high = bar.high;
            const low = bar.low;
            const close = bar.close;

            const formattedOpen = formatOpen(open);
            const formattedHigh = formatHigh(high);
            const formattedLow = formatLow(low);
            const formattedClose = formatClose(close);
            setTooltipHtml(symbolName, time, formattedOpen, formattedHigh, formattedLow, formattedClose);
        };

        chart.subscribeCrosshairMove(updateLegend);
        updateLegend(undefined);
        chart.timeScale().fitContent();

        return () => {
            clearInterval(interval);
            chart.remove();
        };
    }, [theme, legend]);

    return (
        <div className="chartContainerRef" ref={chartContainerRef}></div>
    );
};

export default LightWeightChart;