/* ============================================================ FRUIT MERGE
   AdMob bridge for the Capacitor (Google Play) build.
   ------------------------------------------------------------
   The game's ad layer (detectHost / adAdMob inside index.html) already speaks
   a tiny, provider-agnostic interface:

       window.FM_ADMOB_REWARDED                 -> rewarded ad-unit id (string)
       window.FM_ADMOB_INTERSTITIAL             -> interstitial ad-unit id
       window.FM_ADMOB_BANNER                   -> banner ad-unit id
       window.AdMob.prepareRewardVideoAd({adId})-> Promise
       window.AdMob.showRewardVideoAd()         -> Promise (resolve = reward)
       window.AdMob.prepareInterstitial({adId}) -> Promise
       window.AdMob.showInterstitial()          -> Promise
       window.AdMob.showBanner({adId})          -> Promise (reserves bottom space)

   This file adapts the @capacitor-community/admob plugin (v7) to exactly that
   interface, so the SAME index.html runs unchanged on web, on portals, and on
   the Play Store -- only the ad provider differs.

   It is completely INERT unless this is a native Capacitor build AND the AdMob
   plugin is present. On the web / in the test harness it defines nothing, so
   detectHost() falls through to the built-in "demo" ad and nothing changes.

   Verified against @capacitor-community/admob@7.2.0:
     - plugin global name ............ 'AdMob'  (Capacitor.Plugins.AdMob)
     - methods ....................... initialize / prepareRewardVideoAd /
                                       showRewardVideoAd
     - reward event string ........... 'onRewardedVideoAdReward'
   NOTE: this bridge can only be fully exercised on a real device with real ad
   unit ids; it cannot be verified in the headless test harness.            */
(function () {
  "use strict";
  try {
    var C = window.Capacitor;
    // Web build / test harness -> no Capacitor -> do nothing (demo ad stays).
    if (!C || !C.isNativePlatform || !C.isNativePlatform()) return;
    var P = C.Plugins && C.Plugins.AdMob;
    // Plugin not installed -> do nothing, so detectHost() falls back to demo.
    if (!P || typeof P.prepareRewardVideoAd !== "function") return;

    /* Owner's real AdMob units (confirmed 6 Nov 2026) -- the rewarded unit
       below was earlier mislabelled as Google's test id; it is the real one.
       Production ids live here as defaults; index.html can still override:
           window.FM_ADMOB_REWARDED = "ca-app-pub-XXXX/YYYY";
       (the matching App ID sits in AndroidManifest.xml -- already correct). */
    window.FM_ADMOB_REWARDED =
      window.FM_ADMOB_REWARDED || "ca-app-pub-5002697332409715/7199766849";
    /* Real Interstitial + Banner units (AdMob, 17 Oct 2026). */
    window.FM_ADMOB_INTERSTITIAL =
      window.FM_ADMOB_INTERSTITIAL || "ca-app-pub-5002697332409715/5362484723";
    window.FM_ADMOB_BANNER =
      window.FM_ADMOB_BANNER || "ca-app-pub-5002697332409715/4472074881";

    /* The community plugin must be initialized once before prepare/show.
       initializeForTesting:true forces test ads even with production ids --
       handy while you build; flip to false for a real release.              */
    var initPromise = null;
    function ensureInit() {
      if (!initPromise) {
        initPromise = Promise.resolve()
          .then(function () { return P.initialize({ initializeForTesting: false }); })
          .catch(function () { /* already initialized is fine */ });
      }
      return initPromise;
    }

    /* The reward itself is delivered by an event, not by the show() promise
       (which resolves when the ad closes). Track it so we only pay out when
       the viewer actually earned it.                                        */
    var earned = false;
    try {
      P.addListener("onRewardedVideoAdReward", function () { earned = true; });
    } catch (e) {}

    /* --- UMP consent (GDPR/EEA) gate -------------------------------------
       Google REQUIRES a consent flow for users in the EEA/UK. The plugin
       exposes Google's UMP SDK: requestConsentInfo() fetches the consent
       status from AdMob's message config (AdMob console → Privacy &
       messaging), showConsentForm() shows it if a form is available.
       Every ad call now fails closed: no consent, no ad request.            */
    var consentDone = false;
    function ensureConsent() {
      if (consentDone) return Promise.resolve(true);
      /* plugin without UMP support (old version) -> treat as consented, the
         game must never break because the gate is missing */
      if (typeof P.requestConsentInfo !== "function") { consentDone = true; return Promise.resolve(true); }
      return ensureInit().then(function () {
        return P.requestConsentInfo({ debugGeography: "DISABLED", tagForUnderAgeOfConsent: false });
      }).then(function (info) {
        if (info && info.canRequestAds) { consentDone = true; return true; }
        if (info && info.isConsentFormAvailable && typeof P.showConsentForm === "function") {
          return P.showConsentForm().then(function (i2) {
            consentDone = !!(i2 && i2.canRequestAds);
            return consentDone;
          });
        }
        return false;
      }).catch(function () { return false; });
    }
    function gate(fn) {
      return ensureConsent().then(function (ok) {
        if (!ok) return Promise.reject(new Error("admob: consent not granted / no consent form available"));
        return fn();
      });
    }

    window.AdMob = {
      /* --- full-screen ad between games (game over) --- */
      prepareInterstitial: function (o) {
        var id = (o && o.adId) || window.FM_ADMOB_INTERSTITIAL;
        return gate(function () {
          return P.prepareInterstitial({ adId: id, isTesting: false });
        });
      },
      showInterstitial: function () {
        return ensureInit().then(function () { return P.showInterstitial(); });
      },
      /* --- persistent bottom banner: reserve WebView space so the banner
             never covers the evolution strip / buttons, then reload layout --- */
      showBanner: function (o) {
        return ensureConsent().then(function (ok) {
          if (!ok) return;
          var id = (o && o.adId) || window.FM_ADMOB_BANNER;
          return ensureInit()
          .then(function () {
            return P.showBanner({ adId: id, adSize: "ADAPTIVE_BANNER", position: "BOTTOM_CENTER", isTesting: false });
          })
          .then(function () {
            try {
              if (!document.getElementById("fm-banner-css")) {
                var st = document.createElement("style");
                st.id = "fm-banner-css";
                st.textContent = "body.fm-banner-on #app{padding-bottom:64px}" +
                                 "body.fm-banner-on .ov.home{padding-bottom:64px}";
                document.head.appendChild(st);
              }
              document.body.classList.add("fm-banner-on");
              setTimeout(function () {
                window.dispatchEvent(new Event("resize"));
              }, 400);
            } catch (e) {}
          });
        });
      },
      hideBanner: function () {
        return ensureInit().then(function () { return P.hideBanner(); });
      },
      /* future-proof hook: a "Privacy options" entry point (AdMob
         "Privacy & messaging" config) can call this from game settings */
      showPrivacyOptions: function () {
        return ensureInit().then(function () {
          if (typeof P.showPrivacyOptionsForm === "function") return P.showPrivacyOptionsForm();
        });
      },
      prepareRewardVideoAd: function (o) {
        var id = (o && o.adId) || window.FM_ADMOB_REWARDED;
        return gate(function () {
          return P.prepareRewardVideoAd({ adId: id });
        });
      },
      showRewardVideoAd: function () {
        earned = false;
        return P.showRewardVideoAd().then(function () {
          // Give the reward event a beat to land, then pay out only if earned.
          return new Promise(function (resolve, reject) {
            setTimeout(function () {
              if (earned) resolve(true);
              else reject(new Error("rewarded-ad: no reward earned"));
            }, 300);
          });
        });
      }
    };
  } catch (e) {
    /* Never let ad setup break the game. If anything throws, window.AdMob is
       left undefined and the game simply uses its demo ad.                  */
  }
})();
