
window.onresize = function() {
    if (!document.fullscreenEnabled || window.fullScreen || document.webkitIsFullScreen || document.msFullscreenEnabled){
        resizeCanvas();
    }
};

function runMame(cart, device) {
    var needWasm = 'WebAssembly' in window;
    var mamenesWasmJs = "static/mamenes_wasm.js";
    var mamenesWasmWasm = "static/mamenes_wasm.wasm";
    var mamenesJs = "static/mamenes.js";

    var emulator = new Emulator(document.querySelector("#emularity-canvas"),
        startEmulator,
        new JSMESSLoader(JSMESSLoader.driver(device),
            JSMESSLoader.nativeResolution(640, 480),
            JSMESSLoader.emulatorJS(needWasm ? mamenesWasmJs : mamenesJs),
            JSMESSLoader.emulatorWASM(needWasm && mamenesWasmWasm),
            JSMESSLoader.mountFile("leesoar_com_game",
                JSMESSLoader.fetchFile("Game file",
                    cart)),
            JSMESSLoader.extraArgs(["-cart", "/emulator/leesoar_com_game"])));
    emulator.setScale(3).start({ waitAfterDownloading: true });
    emulator.setSplashImage("static/favicon.ico");
}

function getParams() {
    let params = {};
    window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, k, v) {
        params[k] = v;
    });
    return params;
}

function visitSite() {
    window.location.href = "https://leesoar.com/acfun#support"
}

function startEmulator() {
    console.log("Need help? Go leesoar.com to contact me, or send email to secure@tom.com.");
}

function resizeCanvas() {
    $("#emularity-canvas").width(640);
    $("#emularity-canvas").height(480);
}

function fullScreen() {
    var emulatorObj = document.getElementById("emulator-container");
    if (emulatorObj) {
        var fullScreenObj = emulatorObj.requestFullScreen || emulatorObj.webkitRequestFullscreen || emulatorObj.mozRequestFullScreen || emulatorObj.msRequestFullScreen;
        fullScreenObj && (fullScreenObj.call(emulatorObj),
        (emulatorObj = document.getElementsByClassName("leesoar.com")[0]) && emulatorObj.focus());
    }
}

$(document).ready(function () {
    let cart;
    let device = "nespal";
    let path = getParams()["p"];
    if (path.startsWith("http")) {
        cart = path;
    } else {
        cart = "/api/file?p=" + path;
    }
    runMame(cart, device);
});