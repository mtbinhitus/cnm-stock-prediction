import axios from "axios";

const request = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL,
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

export async function getClosePricePredict(crypto, model, indicator) {
    const response = await request
        .post(`/api/v1/btcsticker/predict`, {
            "sticker": crypto,
            "model": model,
            "indicator": indicator
        })
        .then((res) => {
            let timeMillis = res.data["time"];
            let timeUTC = new Date(timeMillis);
            timeUTC.setHours(timeUTC.getHours() + 7);
            res.data["time"] = timeUTC.getTime() / 1000;
            return { time: res.data["time"], value: res.data["prediction"] };
        })
        .catch((error) => {
            return error;
        });
    return response;
};
