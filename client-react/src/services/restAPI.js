import axios from "axios";

const request = axios.create({
    baseURL: "http://localhost:8000",
    headers: {
        "Content-type": "application/json; charset=UTF-8",
    },
});

export async function getKlineBTCData(limit) {
    const response = await request
        .get(`/api/v1/klines?limit=${limit}`, {})
        .then((res) => {
            res.data.forEach(element => {
                element['time'] = element['time'] / 1000
            });
            return res.data;
        })
        .catch((error) => {
            return error;
        });
    return response;
};

export async function getClosePricePredict(sticker = "BTCUSDT", model = "LSTM", indicator = ["Close", "POC", "MA"]) {
    const response = await request
        .get(`/api/v1/btcsticker/predict`, {
            "sticker": sticker,
            "model": model,
            "indicator": indicator
        })
        .then((res) => {
            return res.data;
        })
        .catch((error) => {
            return error;
        });
    return response;
};