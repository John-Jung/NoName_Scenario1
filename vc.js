Java.perform(function() {
    let WebAppInterface = Java.use("com.example.nonameapp.WebViewActivity$WebAppInterface");
    WebAppInterface["getToken"].implementation = function () {
        console.log(`WebAppInterface.getToken is called`);
        let json = "{\"autoLogin\": true, \"token\": \"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYmNAbmF2ZXIuY29tIiwiaWF0IjoxNzIxODg4MjY5LCJleHAiOjE3MjE5NzQ2Njl9.KSva7IyuK6sqH74yUhkHOnXiomhxS59FQXnRC04fvdE\"}";
        return json;
    };
});