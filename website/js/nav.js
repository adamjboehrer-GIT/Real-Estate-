/* adamboehrer.com — shared navigation behaviour.
   Two independent widgets, both no-ops on pages that do not contain them:
     1. the Guides dropdown in the desktop top nav
     2. the mobile menu panel (the only nav under 760px)                       */
(function () {
  'use strict';

  function wire(root, toggle, panel, onToggle) {
    if (!root || !toggle || !panel) return null;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      panel.hidden = !open;
      if (onToggle) onToggle(open);
    }
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(panel.hidden);
    });
    document.addEventListener('click', function (e) {
      if (!panel.hidden && !root.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { setOpen(false); toggle.focus(); }
    });
    // Any link inside closes the panel. Same-page anchors do not reload, so
    // without this the panel would stay open over the section just jumped to.
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    return setOpen;
  }

  // ---- 1. Guides dropdown (desktop) ----
  var dd = document.querySelector('[data-dd]');
  if (dd) {
    var ddSet = wire(dd, dd.querySelector('[data-dd-toggle]'), dd.querySelector('.nav-dd-menu'));
    if (ddSet) {
      dd.addEventListener('focusout', function () {
        setTimeout(function () {
          if (!dd.contains(document.activeElement)) ddSet(false);
        }, 0);
      });
    }
  }

  // ---- 2. Mobile menu ----
  var mob = document.querySelector('[data-mobnav]');
  if (mob) {
    var panel = document.getElementById('mobile-menu');
    var setMob = wire(mob, mob.querySelector('[data-mobnav-toggle]'), panel, function (open) {
      // Stop the page scrolling behind the open panel.
      document.body.classList.toggle('nav-open', open);
    });
    // If the viewport grows past the mobile breakpoint while the panel is
    // open, close it so the desktop nav is not competing with a stuck panel.
    if (setMob && window.matchMedia) {
      var mq = window.matchMedia('(min-width: 761px)');
      var onChange = function (e) { if (e.matches && panel && !panel.hidden) setMob(false); };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }
})();
