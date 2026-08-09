(function () {
  var el = document.querySelector('.travel-time');
  if (!el) return;
  var startMs = new Date('2017-02-28T07:08:10Z').getTime();
  var yearSeconds = 31557600;
  function tick() {
    var s = Math.floor((Date.now() - startMs) / 1000);
    if (s < 0) s = 0;
    var years = Math.floor(s / yearSeconds);
    var remainder = s - (years * yearSeconds);
    var days = Math.floor(remainder / 86400);
    var hours = Math.floor((remainder % 86400) / 3600);
    var mins = Math.floor((remainder % 3600) / 60);
    var secs = remainder % 60;
    el.querySelector('.tt-years strong').textContent = years;
    el.querySelector('.tt-days strong').textContent = days;
    el.querySelector('.tt-hours strong').textContent = hours;
    el.querySelector('.tt-minutes strong').textContent = mins;
    el.querySelector('.tt-seconds strong').textContent = secs;
  }
  tick();
  setInterval(tick, 1000);
})();
