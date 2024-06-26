import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchIcon from "@mui/icons-material/Search";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import InputBase from "@mui/material/InputBase";
import Toolbar from "@mui/material/Toolbar";
import { alpha, createTheme, styled, ThemeProvider } from "@mui/material/styles";
import ToggleButton from "../components/ToggleButton.js";
import ThemeColors from "../components/ThemeColors.js";
import "../styles.css";

export const ThemeContext = createContext(null);

let color;
let borderColor;

const Search = styled("div")(({ theme }) => ({
    position: "relative",
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    "&:hover": {
        backgroundColor: alpha(theme.palette.common.white, 0.25)
    },
    marginLeft: 0,
    width: "100%",
    [theme.breakpoints.up("sm")]: {
        marginLeft: theme.spacing(1),
        width: "auto"
    }
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
    padding: theme.spacing(0, 2),
    height: "100%",
    position: "absolute",
    pointerEvents: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
    color: "inherit",
    "& .MuiInputBase-input": {
        background: borderColor,
        borderRadius: "19.5px",
        padding: theme.spacing(1, 1, 1, 0),
        paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        transition: theme.transitions.create("width"),
        width: "100%",
        [theme.breakpoints.up("sm")]: {
            width: "20ch",
            // "&:focus": {
            //     width: "30ch"
            // }
        }
    }
}));

function Header({ updateTheme, theme, showSearchBar }) {
    const toggleTheme = () => {
        const newTheme = theme === "light" ? "dark" : "light";
        updateTheme(newTheme);
    };

    color = theme === "dark" ? ThemeColors.grayishBlue : ThemeColors.darkBlue;
    borderColor = theme === "dark" ? ThemeColors.darkBlue2 : ThemeColors.grayishBlue2;

    const commonButtonStyle = {
        fontWeight: 600,
        fontSize: 20,
        background: "transparent !important",
        textTransform: "none",
        borderRadius: "0px",
        "&:hover": {
            color: ThemeColors.vividBlue
        },
        "&:active": {
            color: color
        }
    };

    const themeMUI = createTheme({
        components: {
            MuiButton: {
                variants: [{
                    props: { variant: "light" },
                    style: {
                        ...commonButtonStyle,
                        color: ThemeColors.darkBlue
                    }
                },
                {
                    props: { variant: "dark" },
                    style: {
                        ...commonButtonStyle,
                        color: ThemeColors.grayishBlue
                    }
                }]
            }
        }
    });

    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        navigate(`/search/${encodeURIComponent(searchQuery)}`);
        setSearchQuery("");
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            <ThemeProvider theme={themeMUI}>
                <AppBar position="static" sx={{ background: "transparent" }}>
                    <Container id="header-1-1" maxWidth="xl">
                        <Toolbar disableGutters>
                            <Box id="header-1-3" sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
                                <Button
                                    className="button"
                                    variant={theme}
                                    href="/"
                                >Dashboard</Button>

                                <Button
                                    className="button"
                                    variant={theme}
                                    href="/prediction"
                                >Prediction</Button>
                            </Box>

                            {showSearchBar && <form onSubmit={handleSubmit}>
                                <Search id="header-1-2" style={{ background: "transparent" }}>
                                    <SearchIconWrapper>
                                        <SearchIcon style={{ color: color, zIndex: 1, opacity: 0.42 }} />
                                    </SearchIconWrapper>

                                    <StyledInputBase
                                        placeholder="BINANCE:BTCUSDT"
                                        style={{ color: color }}
                                        value={searchQuery}
                                        onChange={(event) => setSearchQuery(event.target.value)}
                                    ></StyledInputBase>
                                </Search>
                            </form>}

                            <ToggleButton
                                onChange={toggleTheme}
                                checked={theme === "dark"}
                            ></ToggleButton>
                        </Toolbar>
                    </Container>
                </AppBar>
            </ThemeProvider>
        </ThemeContext.Provider>
    );
};

export default Header;