import Cookies from "js-cookie";
import {jwtDecode} from "jwt-decode"; // jwt-decode is required to decode the token

function checkAuthorizaion() {
    console.log("Checking authorization");
    const token = Cookies.get("token");
    if (token) {
        try {
            const decodedToken = jwtDecode(token);
            const currentTime = Date.now() / 1000;
            if (decodedToken.exp > currentTime) {
                sessionStorage.setItem("token", token);
                console.log("Authorization successful");
                return true;
            } else {
                return false;
            }
        } catch (error) {
            error;
            // token is invalid or expired
            return false;
        }
    } else {
        return false;
    }
}

function loadSessionToken() {
    const token = sessionStorage.getItem("token");
    if (token) {
        return token;
    } else {
        return null;
    }
}

function logout() {
    Cookies.remove("username", {SameSite: 'Lax'});
    Cookies.remove("token", {SameSite: 'Lax'});
    sessionStorage.removeItem("token");
}

function getUserId(){
    const token = sessionStorage.getItem("token");
    if (token) {
        const decodedToken = jwtDecode(token);
        return decodedToken.sub;
    } else {
        return null;
    }
}
export { checkAuthorizaion, logout, loadSessionToken,getUserId };