(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var buttons = document.querySelectorAll("[data-filter]");
  var cards = document.querySelectorAll("[data-course]");
  if (!buttons.length || !cards.length) return;

  function apply() {
    var currentCourse = document.body.dataset.course || "all";
    var currentStatus = document.body.dataset.status || "all";
    cards.forEach(function (card) {
      var show =
        (currentCourse === "all" || card.dataset.course === currentCourse) &&
        (currentStatus === "all" || card.dataset.status === currentStatus);
      card.classList.toggle("hidden", !show);
    });
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var kind = button.dataset.filter;
      document.body.dataset[kind] = button.dataset.value;
      document.querySelectorAll('[data-filter="' + kind + '"]').forEach(function (peer) {
        peer.setAttribute("aria-pressed", peer === button ? "true" : "false");
      });
      apply();
    });
  });
})();
