Java.perform(() => {
    let RootFridaCheckActivity = Java.use("com.example.nonameapp.RootFridaCheckActivity");
    RootFridaCheckActivity["CheckState"].implementation = function (context) {
        console.log(`RootFridaCheckActivity.CheckState is called: context=${context}`);
        let result = this["CheckState"](context);
        result = true
        console.log(`RootFridaCheckActivity.CheckState result=${result}`);
        return result;
    };
});