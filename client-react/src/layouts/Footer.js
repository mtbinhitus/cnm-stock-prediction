import GitHubIcon from "@mui/icons-material/GitHub";
import OndemandVideoIcon from "@mui/icons-material/OndemandVideo";
import { BottomNavigation, BottomNavigationAction } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import ThemeColors from "../components/ThemeColors.js";
import "../styles.css";

function Footer({ theme }) {
    const color = theme === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;

    const themeMUI = createTheme({
        components: {
            MuiBottomNavigationAction: {
                variants: [{
                    props: { variant: "hover" },
                    style: {
                        color: color,
                        "&:hover": {
                            color: ThemeColors.vividBlue
                        },
                        "&:active": {
                            color: color
                        }
                    }
                }]
            }
        }
    });

    return (
        <ThemeProvider theme={themeMUI}>
            <BottomNavigation showLabels style={{ background: "transparent" }}>
                <BottomNavigationAction
                    variant="hover"
                    label="Github"
                    href="https://github.com/mtbinhitus/cnm-stock-prediction"
                    target="_blank" rel="noopener noreferrer"
                    icon={<GitHubIcon />}
                ></BottomNavigationAction>

                <BottomNavigationAction
                    variant="hover"
                    label="Demo"
                    href="https://drive.google.com/drive/folders/1i25SXU7x9VsUxhcuKBtMTy3WVfSCu1vx?usp=drive_link"
                    target="_blank" rel="noopener noreferrer"
                    icon={<OndemandVideoIcon />}
                ></BottomNavigationAction>
            </BottomNavigation>
        </ThemeProvider>
    );
};

export default Footer;