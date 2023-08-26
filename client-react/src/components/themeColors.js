import "../styles.css";

const themeColors = {
    darkBlue: getComputedStyle(document.body).getPropertyValue("--darkBlue"),
    darkBlue2: getComputedStyle(document.body).getPropertyValue("--darkBlue2"),
    grayishBlue: getComputedStyle(document.body).getPropertyValue("--grayishBlue"),
    grayishBlue2: getComputedStyle(document.body).getPropertyValue("--grayishBlue2"),
    white: getComputedStyle(document.body).getPropertyValue("--white"),
    vividBlue: getComputedStyle(document.body).getPropertyValue("--vividBlue"),
    candlePositive: getComputedStyle(document.body).getPropertyValue("--candlePositive"),
    candleNegative: getComputedStyle(document.body).getPropertyValue("--candleNegative")
};

export default themeColors;
