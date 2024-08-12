Java.perform(function() {
    let WebAppInterface = Java.use("com.example.nonameapp.WebViewActivity$WebAppInterface");
    WebAppInterface["getToken"].implementation = function () {
        console.log(`WebAppInterface.getToken is called`);
        let json = "{\"autoLogin\": true, \"token\": \"탈취한 jwt 토큰"}";
        return json;
    };
});