/*
 * MinaTech MobileRecruit — 共通機能JS
 *
 * 全LPで共通の機能を1ファイルに集約：
 *  1) UTMパラメータ取得 → sessionStorage保存 → 応募/LINEリンクへ伝播
 *  2) data-action="apply" / "line" のhrefを config.js のURLに差し込み
 *  3) FAQアコーディオン開閉
 *  4) GA4 / Meta Pixel の遅延読み込み（IDが実値のときのみ作動）
 *  5) CTAクリック計測
 *
 * body[data-lp] でLP識別。calls trackEvent('cta_apply_click', { lp })。
 */
(function () {
  'use strict';

  var cfg = window.RECRUIT_CONFIG || {};
  var lp = (document.body && document.body.dataset && document.body.dataset.lp) || 'unknown';

  // ---- UTM capture & persist ----------------------------------------------
  function captureUTM() {
    var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'yclid'];
    var url;
    try { url = new URL(window.location.href); } catch (e) { return {}; }
    var fromUrl = {};
    utmKeys.forEach(function (k) {
      var v = url.searchParams.get(k);
      if (v) fromUrl[k] = v;
    });
    if (Object.keys(fromUrl).length) {
      try { sessionStorage.setItem('mr_utm', JSON.stringify(fromUrl)); } catch (e) {}
      return fromUrl;
    }
    try { return JSON.parse(sessionStorage.getItem('mr_utm') || '{}'); }
    catch (e) { return {}; }
  }
  var utm = captureUTM();

  // ---- URL with UTM forwarded ---------------------------------------------
  function isPlaceholder(v) {
    return !v || /PLACEHOLDER|XXXX/i.test(v);
  }
  function buildActionUrl(baseUrl, action) {
    if (isPlaceholder(baseUrl)) return null;
    try {
      var u = new URL(baseUrl);
      Object.keys(utm).forEach(function (k) { u.searchParams.set(k, utm[k]); });
      u.searchParams.set('mr_lp', lp);
      u.searchParams.set('mr_action', action);
      return u.toString();
    } catch (e) { return baseUrl; }
  }

  // ---- Wire data-action links ---------------------------------------------
  function wireActionLinks() {
    var pairs = [
      { sel: '[data-action="apply"]', base: cfg.applyUrl, event: 'cta_apply_click' },
      { sel: '[data-action="line"]',  base: cfg.lineUrl,  event: 'cta_line_click' }
    ];
    pairs.forEach(function (p) {
      var url = buildActionUrl(p.base, p.sel.indexOf('apply') > -1 ? 'apply' : 'line');
      document.querySelectorAll(p.sel).forEach(function (el) {
        if (url) {
          el.href = url;
          el.setAttribute('target', '_blank');
          el.setAttribute('rel', 'noopener');
        } else {
          // プレースホルダのままなら、押下時に注意表示
          el.addEventListener('click', function (e) {
            e.preventDefault();
            alert('応募リンクは公開準備中です。設定完了までお待ちください。');
          });
        }
        el.addEventListener('click', function () { trackEvent(p.event, { lp: lp }); });
      });
    });
  }

  // ---- FAQ accordion ------------------------------------------------------
  function wireFaq() {
    document.querySelectorAll('.faq-item').forEach(function (item) {
      var q = item.querySelector('.faq-q');
      if (q) q.addEventListener('click', function () { item.classList.toggle('open'); });
    });
  }

  // ---- Scroll reveal (IntersectionObserver based) -------------------------
  function initScrollReveal() {
    var els = document.querySelectorAll('[data-reveal], [data-reveal-stagger]');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
    els.forEach(function (el) { observer.observe(el); });
  }

  // ---- Header shadow on scroll -------------------------------------------
  function initHeaderShadow() {
    var header = document.querySelector('.lp-header');
    if (!header) return;
    var update = function () {
      if (window.scrollY > 12) header.classList.add('scrolled');
      else header.classList.remove('scrolled');
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  // ---- GA4 ----------------------------------------------------------------
  function loadGA4() {
    if (isPlaceholder(cfg.ga4Id)) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.ga4Id);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', cfg.ga4Id, { page_path: location.pathname, mr_lp: lp });
  }

  // ---- Meta Pixel ---------------------------------------------------------
  function loadPixel() {
    if (isPlaceholder(cfg.metaPixelId)) return;
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq('init', cfg.metaPixelId);
    window.fbq('track', 'PageView');
  }

  function trackEvent(name, params) {
    if (window.gtag) window.gtag('event', name, params);
    if (window.fbq && name.indexOf('cta_') === 0) window.fbq('track', 'Lead', params);
  }

  // ---- Init ---------------------------------------------------------------
  function init() {
    wireActionLinks();
    wireFaq();
    initScrollReveal();
    initHeaderShadow();
    loadGA4();
    loadPixel();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
