import axios from "axios";

const request = axios.create({
    baseURL: "http://localhost:8000",
    headers: {
        "Content-type": "application/json; charset=UTF-8"
    }
});

export async function getKlineBTCData(limit) {
    const response = await request
        .get(`/api/v1/klines?limit=${limit}`, {})
        .then((res) => {
            res.data.forEach(element => {
                let timeMillis = element["time"];
                let timeUTC = new Date(timeMillis);
                timeUTC.setHours(timeUTC.getHours() + 7);
                element["time"] = timeUTC.getTime() / 1000;
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