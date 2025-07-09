odoo.define(
  "website_frequently_bought_together.fbt_carousel",
  function (require) {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
      var section = document.querySelector(".oe_fbt_section");
      if (!section) return;
      var carousel = section.querySelector(".fbt-carousel");
      var btnPrev = section.querySelector(".fbt-carousel-nav.prev");
      var btnNext = section.querySelector(".fbt-carousel-nav.next");
      if (!carousel || !btnPrev || !btnNext) return;
      btnPrev.addEventListener("click", function () {
        carousel.scrollBy({ left: -280, behavior: "smooth" });
      });
      btnNext.addEventListener("click", function () {
        carousel.scrollBy({ left: 280, behavior: "smooth" });
      });
    });
  }
);
