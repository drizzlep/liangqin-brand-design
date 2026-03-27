const reveals = document.querySelectorAll('.reveal');
const spySections = document.querySelectorAll('[data-spy-section]');
const spyLinks = document.querySelectorAll('.guide-nav-link');
const themeToggleButtons = document.querySelectorAll('.theme-toggle-button');
const themeMedia = window.matchMedia('(prefers-color-scheme: dark)');
const THEME_STORAGE_KEY = 'liangqin-theme-preference';
const DEFAULT_THEME = 'system';
const VALID_THEMES = new Set(['system', 'light', 'dark']);

const getStoredTheme = () => {
  try {
    const value = window.localStorage.getItem(THEME_STORAGE_KEY) || DEFAULT_THEME;
    return VALID_THEMES.has(value) ? value : DEFAULT_THEME;
  } catch {
    return DEFAULT_THEME;
  }
};

const setStoredTheme = (value) => {
  try {
    window.localStorage.setItem(THEME_STORAGE_KEY, value);
  } catch {
    // Ignore write failures so theme switching still works for the current session.
  }
};

const resolveTheme = (preference) => {
  if (preference === 'system') {
    return themeMedia.matches ? 'dark' : 'light';
  }

  return preference;
};

const syncThemeButtons = (preference) => {
  themeToggleButtons.forEach((button) => {
    const isActive = button.dataset.themeValue === preference;
    button.classList.toggle('is-active', isActive);
    button.setAttribute('aria-pressed', String(isActive));
  });
};

const applyTheme = (preference = getStoredTheme()) => {
  const resolvedTheme = resolveTheme(preference);

  document.documentElement.dataset.themePreference = preference;
  document.documentElement.dataset.themeResolved = resolvedTheme;
  syncThemeButtons(preference);
};

const enableThemeToggle = () => {
  applyTheme();

  if (themeToggleButtons.length) {
    themeToggleButtons.forEach((button) => {
      button.addEventListener('click', () => {
        const nextTheme = button.dataset.themeValue;
        if (!VALID_THEMES.has(nextTheme)) {
          return;
        }

        setStoredTheme(nextTheme);
        applyTheme(nextTheme);
      });
    });
  }

  const handleSystemThemeChange = () => {
    if (getStoredTheme() === 'system') {
      applyTheme('system');
    }
  };

  if (typeof themeMedia.addEventListener === 'function') {
    themeMedia.addEventListener('change', handleSystemThemeChange);
  } else if (typeof themeMedia.addListener === 'function') {
    themeMedia.addListener(handleSystemThemeChange);
  }
};

const enableReveal = () => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    reveals.forEach((item) => item.classList.add('is-visible'));
    return;
  }

  const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

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

    const rect = item.getBoundingClientRect();
    const isInitiallyVisible = rect.top < viewportHeight * 0.92 && rect.bottom > 0;

    if (isInitiallyVisible) {
      item.classList.add('is-visible');
      return;
    }

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
  enableThemeToggle();
  enableReveal();
  enableScrollSpy();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot, { once: true });
} else {
  boot();
}
