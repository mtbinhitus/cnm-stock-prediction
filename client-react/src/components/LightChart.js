import { useEffect, useRef } from "react";
import { ColorType, createChart } from "lightweight-charts";
import themeColors from "./themeColors";

const LightChart = ({ theme }) => {
    const chartContainerRef = useRef();
    const legend = document.createElement("div");

    useEffect(() => {
        // const data = [
        //     { time: "2018-12-22", value: 75.16 },
        //     { time: "2018-12-23", value: 45.12 },
        //     { time: "2018-12-24", value: 60.71 },
        //     { time: "2018-12-25", value: 68.26 },
        //     { time: "2018-12-26", value: 67.71 },
        //     { time: "2018-12-27", value: 91.04 },
        //     { time: "2018-12-28", value: 111.51 },
        //     { time: "2018-12-29", value: 131.33 },
        //     { time: "2018-12-30", value: 106.33 },
        //     { time: "2018-12-31", value: 109.87 }
        // ];

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
            height: 400
        });

        // const series = chart.addLineSeries();
        const series = chart.addCandlestickSeries();
        series.setData(data);

        function nextBusinessDay(time) {
            var date = new Date();
            date.setUTCFullYear(time.year);
            date.setUTCMonth(time.month - 1);
            date.setUTCDate(time.day + 1);
            date.setUTCHours(0, 0, 0, 0);

            return {
                year: date.getUTCFullYear(),
                month: date.getUTCMonth() + 1,
                day: date.getUTCDate()
            };
        };

        const symbolName = "BINANCE:BTCUSDT";
        legend.style = `position: absolute; left: 12px; top: 12px; z-index: 1; font-size: 14px; line-height: 18px; font-weight: 300;`;
        legend.style.color = textColor;
        chartContainerRef.current.appendChild(legend);

        const getLastBar = series => {
            const lastIndex = series.dataByIndex(Math.Infinity, -1);
            return series.dataByIndex(lastIndex);
        };

        const formatPrice = price => (Math.round(price * 100) / 100).toFixed(2);
        const setTooltipHtml = (name, date, price) => {
            legend.innerHTML = `<div style="font-size: 24px; margin: 4px 0px;">${name}</div><div style="font-size: 22px; margin: 4px 0px;">${price}</div><div>${date}</div>`;
        };

        const updateLegend = param => {
            const validCrosshairPoint = !(
                param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0
            );
            const bar = validCrosshairPoint ? param.seriesData.get(series) : getLastBar(series);
            const time = bar.time;
            const price = bar.value !== undefined ? bar.value : bar.close;
            const formattedPrice = formatPrice(price);
            setTooltipHtml(symbolName, time, formattedPrice);
        };

        chart.subscribeCrosshairMove(updateLegend);
        updateLegend(undefined);
        chart.timeScale().fitContent();

        setInterval(() => {
            const lastItemTime = data[data.length - 1].time;
            const nextTime = nextBusinessDay(lastItemTime);

            // const newCandle = {
            //     time: nextTime,
            //     value: 58 + Math.random() * 2
            // };

            const newCandle = {
                time: nextTime,
                high: 58 + Math.random() * 2,
                open: 52 + Math.random() * 6,
                low: 50 + Math.random() * 2,
                close: 52 + Math.random() * 6
            };

            series.update(newCandle);
            data.push(newCandle);
        }, 1000);

        return () => {
            chart.remove();
        };
    }, [theme, legend]);

    return (
        <div className="chartContainerRef" ref={chartContainerRef}></div>
    );
};

export default LightChart;