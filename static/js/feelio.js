/* Feelio — Main JavaScript */
'use strict';

// ── Auto-dismiss alerts after 5s ────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    document.querySelectorAll('.alert.fade.show').forEach(el => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    });
  }, 5000);

  // ── Active nav links (bottom nav) ─────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.bottom-nav a').forEach(a => {
    if (a.getAttribute('href') && path.startsWith(a.getAttribute('href')) && a.getAttribute('href') !== '/') {
      a.classList.add('active');
    }
  });

  // ── Mood label click → select radio ───────────────
  document.querySelectorAll('.mood-label').forEach(label => {
    label.addEventListener('click', () => {
      document.querySelectorAll('.mood-label').forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');
    });
  });

  // ── EPDS option highlight on click ────────────────
  document.querySelectorAll('.epds-option').forEach(opt => {
    opt.addEventListener('click', () => {
      const name = opt.querySelector('input').name;
      document.querySelectorAll(`.epds-option input[name="${name}"]`).forEach(i => {
        i.closest('.epds-option').style.borderColor = '';
        i.closest('.epds-option').style.background = '';
      });
      opt.style.borderColor = 'var(--primary)';
      opt.style.background = 'var(--bg1)';
    });
  });

  // ── Offline banner ────────────────────────────────
  function showOfflineBanner() {
    let banner = document.getElementById('offlineBanner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'offlineBanner';
      banner.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#AD1457;color:#fff;text-align:center;padding:8px;font-weight:600;font-size:0.9rem;z-index:9999;';
      banner.innerHTML = '<i class="fa-solid fa-wifi-slash me-2"></i>You are offline. Your data will sync when reconnected.';
      document.body.prepend(banner);
    }
  }
  function hideOfflineBanner() {
    const b = document.getElementById('offlineBanner');
    if (b) b.remove();
  }
  window.addEventListener('offline', showOfflineBanner);
  window.addEventListener('online', hideOfflineBanner);
  if (!navigator.onLine) showOfflineBanner();
});
