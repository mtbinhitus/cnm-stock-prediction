import { useEffect, useRef } from "react";
import { ColorType, createChart } from "lightweight-charts";
import themeColors from "./themeColors";

const LightChart = () => {
    const chartContainerRef = useRef();

    useEffect(() => {
        const data = [
            { time: '2018-12-22', open: 75.16, high: 82.84, low: 36.16, close: 45.72 },
            { time: '2018-12-23', open: 45.12, high: 53.90, low: 45.12, close: 48.09 },
            { time: '2018-12-24', open: 60.71, high: 60.71, low: 53.39, close: 59.29 },
            { time: '2018-12-25', open: 68.26, high: 68.26, low: 59.04, close: 60.50 },
            { time: '2018-12-26', open: 67.71, high: 105.85, low: 66.67, close: 91.04 },
            { time: '2018-12-27', open: 91.04, high: 121.40, low: 82.70, close: 111.40 },
            { time: '2018-12-28', open: 111.51, high: 142.83, low: 103.34, close: 131.25 },
            { time: '2018-12-29', open: 131.33, high: 151.17, low: 77.68, close: 96.43 },
            { time: '2018-12-30', open: 106.33, high: 110.20, low: 90.39, close: 98.10 },
            { time: '2018-12-31', open: 109.87, high: 114.69, low: 85.66, close: 111.26 }
        ];

        const chart = createChart(chartContainerRef.current);
        chart.applyOptions({
            layout: {
                background: {
                    type: ColorType.Solid,
                    color: themeColors.white
                },
                textColor: themeColors.darkBlue
            },
            width: chartContainerRef.current.clientWidth,
            height: 300
        });

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

        setInterval(() => {
            const lastItemTime = data[data.length - 1].time;
            const nextTime = nextBusinessDay(lastItemTime);

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
    }, []);

    return (
        <div className="chartContainerRef" ref={chartContainerRef}></div>
    );
};

export default LightChart;