const reveals = document.querySelectorAll('.reveal');
const spySections = document.querySelectorAll('[data-spy-section]');
const spyLinks = document.querySelectorAll('.guide-nav-link');

const enableReveal = () => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    reveals.forEach((item) => item.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.12,
      rootMargin: '0px 0px -8% 0px',
    }
  );

  reveals.forEach((item, index) => {
    item.style.transitionDelay = `${Math.min(index * 35, 280)}ms`;
    observer.observe(item);
  });
};

const enableScrollSpy = () => {
  if (!spySections.length || !spyLinks.length || !('IntersectionObserver' in window)) {
    return;
  }

  const linkMap = new Map(
    [...spyLinks].map((link) => [link.getAttribute('href')?.replace('#', ''), link])
  );

  const activate = (id) => {
    spyLinks.forEach((link) => {
      link.classList.toggle('is-active', link.getAttribute('href') === `#${id}`);
    });
  };

  const observer = new IntersectionObserver(
    (entries) => {
      const visibleEntries = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

      if (!visibleEntries.length) {
        return;
      }

      const activeId = visibleEntries[0].target.id;
      if (linkMap.has(activeId)) {
        activate(activeId);
      }
    },
    {
      threshold: [0.2, 0.4, 0.6],
      rootMargin: '-12% 0px -55% 0px',
    }
  );

  spySections.forEach((section) => observer.observe(section));

  const hash = window.location.hash.replace('#', '');
  if (hash && linkMap.has(hash)) {
    activate(hash);
  } else if (spySections[0]) {
    activate(spySections[0].id);
  }
};

const boot = () => {
  enableReveal();
  enableScrollSpy();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot, { once: true });
} else {
  boot();
}
