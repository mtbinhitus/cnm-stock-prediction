import React, { useEffect } from 'react';

const TradingViewChart = () => {
    useEffect(() => {
        const widgetOptions = {
            widgetType: 'widget',
            autosize: true,
            symbol: 'BINANCE:BTCUSDT',
            interval: '240',
            timezone: 'Etc/UTC',
            theme: 'dark',
            style: '1',
            locale: 'en',
            enable_publishing: false,
            hide_side_toolbar: false,
            allow_symbol_change: true,
            container_id: 'tv_chart_container',
            watchlist: [
                "BINANCE:BTCUSDT",
                "BINANCE:ETHUSDT",
                "BINANCE:XRPUSDT",
                "BINANCE:NULSUSDT",
                "BINANCE:LTCUSDT",
                "BINANCE:COSUSDT",
                "BINANCE:EOSUSDT",
                "BINANCE:BCHUSDT",
                "BINANCE:THETAUSDT",
            ],
            details: true,
            hotlist: true,
            calendar: true,
        };

        const script = document.createElement('script');
        script.src = 'https://s3.tradingview.com/tv.js';
        script.async = true;
        script.onload = () => {
            new window.TradingView.widget(widgetOptions);
        };

        document.body.appendChild(script);

        return () => {
            document.body.removeChild(script);
        };
    }, []);

    <div id="tv_chart_container" style={{ width: '100%', height: '500px' }} />
};

export default TradingViewChart;