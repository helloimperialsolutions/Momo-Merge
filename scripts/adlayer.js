/* ---------- 13b. ads — one codebase, every surface ---------- */
/* The same index.html ships to the web, to the Play Store via Capacitor, and
   to portals. Only the ad provider differs, so it is the ONLY thing that
   branches. Detection order matters: an explicit override wins (tests), then
   whichever SDK is actually present, then the native plugin, then the demo. */
function detectHost(){
  try{
    if(window.FM_HOST) return window.FM_HOST;
    var CG=window.CrazyGames&&window.CrazyGames.SDK;
    if(CG&&CG.ad&&CG.ad.requestAd) return "crazygames";
    if(window.gdsdk&&window.gdsdk.showAd) return "gamedistribution";
    if(window.Capacitor&&window.Capacitor.isNativePlatform&&
       window.Capacitor.isNativePlatform()&&window.AdMob) return "admob";
  }catch(e){}
  return "demo";
}
var HOST=detectHost();

/* Snapshot the state we came from. The game can legitimately be paused before
   an ad starts -- hidden tab (visibilitychange), or the volume popup -- and if
   adResume blindly forced state="play" the game would resume behind an overlay
   that is still on screen. So restore exactly what we paused from, and only
   force "play" if something else moved the state out from under us. */
var adPrevState=null;
function adPause(){
  if(state==="play"){ adPrevState="play"; state="pause"; }
  else if(adPrevState===null){ adPrevState=state; }
}
function adResume(){
  var back=adPrevState===null?"play":adPrevState; adPrevState=null;
  if(state==="menu"||state==="over") return;
  /* If the tab went away while the ad was up, the visibilitychange handler
     already paused the game underneath it. Restoring "play" here would leave a
     hidden tab burning frames, physics and battery with nobody watching. */
  if(document.hidden||volOpen) back="pause";
  state=back; updatePowerUI();
}
var adMuted=false;
function adMute(on){ adMuted=on; }

function rewardFailed(){
  document.getElementById("adOv").classList.add("hide");
  adResume();
  notify(T("adFail"));
}
function rewardGranted(cb){
  document.getElementById("adOv").classList.add("hide");
  adResume(); sfxCoin(); buzz(20); cb();
}

/* CrazyGames v3: reward ONLY on adFinished. adError must never reward, and the
   game must survive adsDisabledBasicLaunch / unfilled / adblock / adCooldown. */
function adCrazyGames(cb){
  var CG=window.CrazyGames.SDK, done=false;
  CG.ad.requestAd("rewarded",{
    adStarted:function(){ adPause(); adMute(true); },
    adFinished:function(){ if(done) return; done=true; adMute(false); rewardGranted(cb); },
    adError:function(){ if(done) return; done=true; adMute(false); rewardFailed(); }
  });
}

/* GameDistribution: grant once, only on SDK_REWARDED_WATCH_COMPLETE. Deadlines
   so a lost event can never leave the game stuck paused. */
function adGameDistribution(cb){
  var granted=false, finished=false;
  var opt=window.GD_OPTIONS;
  var prev=opt&&opt.onEvent;
  var tFail=0, tDone=0;
  var settle=function(ok){
    if(finished) return; finished=true;
    if(opt) opt.onEvent=prev;
    clearTimeout(tFail); clearTimeout(tDone);
    /* `ok` is settle(granted) from the promise/95s path, so by the time we get
       here ok===true already means the watch-complete event was seen. The old
       guard was `ok&&!granted` -- but the event handler sets granted=true
       first, so that condition was ALWAYS false on the success path and every
       completed GameDistribution ad paid the player nothing. The `finished`
       latch above is what prevents a double grant, not this check. */
    if(ok){ granted=true; rewardGranted(cb); } else rewardFailed();
  };
  if(opt) opt.onEvent=function(ev){
    var n=ev&&ev.name;
    if(n==="SDK_GAME_PAUSE") adPause();
    else if(n==="SDK_GAME_START") adResume();
    else if(n==="SDK_REWARDED_WATCH_COMPLETE") granted=true;
    if(prev) prev(ev);
  };
  tFail=setTimeout(function(){ settle(false); },20000);    // ad never started
  tDone=setTimeout(function(){ settle(granted); },95000);  // never handed back
  try{
    window.gdsdk.showAd("rewarded")
      .then(function(){ settle(granted); })
      .catch(function(){ settle(false); });
  }catch(e){ settle(false); }
}

function adAdMob(cb){
  var id=window.FM_ADMOB_REWARDED||"";
  if(!id){ rewardFailed(); return; }
  window.AdMob.prepareRewardVideoAd({adId:id})
    .then(function(){ return window.AdMob.showRewardVideoAd(); })
    .then(function(){ rewardGranted(cb); })
    .catch(function(){ rewardFailed(); });
}

/* Browser / desktop fallback: the demo countdown. Also what a portal shows
   during Basic Launch, when its SDK deliberately serves no ads. */
function adDemo(cb){
  var ov=document.getElementById("adOv"), cnt=document.getElementById("adCount");
  ov.classList.remove("hide");
  var n=3; cnt.textContent=n;
  var iv=setInterval(function(){
    n--;
    if(n<=0){ clearInterval(iv); rewardGranted(cb); }
    else cnt.textContent=n;
  },800);
}

function requestReward(cb){
  HOST=detectHost();
  if(HOST==="crazygames")       return adCrazyGames(cb);
  if(HOST==="gamedistribution") return adGameDistribution(cb);
  if(HOST==="admob")            return adAdMob(cb);
  return adDemo(cb);
}

/* Portal lifecycle: CrazyGames measures the initial download on the first
   gameplayStart, so omitting it is not harmless. Both are guarded so the
   self-contained offline build keeps working with no SDK present. */
function portalGameplayStart(){
  try{
    if(window.CrazyGames&&window.CrazyGames.SDK&&window.CrazyGames.SDK.game&&
       window.CrazyGames.SDK.game.gameplayStart) window.CrazyGames.SDK.game.gameplayStart();
  }catch(e){}
}
function portalGameplayStop(){
  try{
    if(window.CrazyGames&&window.CrazyGames.SDK&&window.CrazyGames.SDK.game&&
       window.CrazyGames.SDK.game.gameplayStop) window.CrazyGames.SDK.game.gameplayStop();
  }catch(e){}
}
/* Spending order matters: the free per-round allotment first, then the
   persistent stock the player actually PAID diamonds for, then an ad. Skipping
   the middle step would make a purchase worthless -- which is exactly the bug
   this replaces (bought powers used to vanish on the next newRound). */
function spendPower(k,fn){
  if(powers[k]>0){ powers[k]--; fn(); return; }
  if(store.inv&&store.inv[k]>0){ store.inv[k]--; save(); updatePowerUI(); refreshEcon(); fn(); return; }
  requestReward(fn);
}
/* A purchased bomb was previously a dead purchase: store.inv.bomb incremented
   and the shop showed "Owned: N", but nothing in the game ever consumed it.
   This turns the fruit currently held in the aim slot into a bomb, which is the
   same {st:2,sp:1} shape the random queue already produces -- so the existing
   fuse/explode path handles it with no special-casing. */
document.getElementById("bombBtn").addEventListener("click",function(){
  if(state!=="play") return;
  if(cur.sp===1){ notify(T("bombAlready")); return; }
  if(!(store.inv&&store.inv.bomb>0)){ notify(T("bombNone")); requestReward(function(){
    if(store.inv) { store.inv.bomb++; save(); updatePowerUI(); refreshEcon(); }
  }); return; }
  store.inv.bomb--; save();
  cur={st:2,sp:1};
  drawNext(); updatePowerUI(); refreshEcon();
  sfxUnlock(); buzz([20,20]);
  notify(T("bombReady"));
});
document.getElementById("sweepBtn").addEventListener("click",function(){
  if(state!=="play") return;
  if(fruits.length===0){ notify(T("emptyBox")); return; }
  spendPower("sweep",doSweep);
});
document.getElementById("undoBtn").addEventListener("click",function(){
  if(state!=="play") return;
  if(!lastDrop||fruits.indexOf(lastDrop.body)<0){ notify(T("undoNo")); return; }
  spendPower("undo",doUndo);
});
document.getElementById("freezeBtn").addEventListener("click",function(){
  if(state!=="play") return;
  if(frozen()){ notify("Pehle se frozen hai!"); return; }
  spendPower("freeze",doFreeze);
});

/* ---------- 12. achievements ---------- */
/* Names live in the i18n table (T(key)); only the condition and the icon stay
   here, so adding a language never means editing this object. */
var ACH={
  a1:{i:"🧩",r:10,c:function(){return store.merges>=1;}},
  a2:{i:"💯",r:20,c:function(){return score>=1000||store.best>=1000;}},
  a3:{i:"🔥",r:40,c:function(){return score>=5000||store.best>=5000;}},
  a4:{i:"🍉",r:15,c:function(){return store.melons>=1;}},
  a5:{i:"👑",r:40,c:function(){return store.melons>=5;}},
  a6:{i:"⚡",r:25,c:function(){return comboCount>=9;}},
  a7:{i:"💥",r:30,c:function(){return store.merges>=100;}},
  a8:{i:"🎮",r:20,c:function(){var p=store.powersUsed;return p.s>0&&p.u>0&&p.f>0;}},
  a9:{i:"🎲",r:15,c:function(){return !!store.lastDaily;}}
};
function achName(k){ return T(k); }
function achCount(){ var n=0; for(var k in ACH) if(store.ach[k]) n++; return n; }
function checkAch(force){
  for(var k in ACH){
    if(!store.ach[k]&&ACH[k].c()){
      store.ach[k]=true; sessionAch.push(achName(k));
      notify("🏅 "+achName(k)+"! Collect your 💎"); sfxUnlock(); buzz([30,30,30]);
      save(); refreshStartChips(); buildAchGrid();
      /* Payout now happens in the achievements popup via a Collect button, so
         the player actively claims each reward. store.ach guards the unlock. */
    }
  }
}
/* The home message line has a fixed CSS height, so writing to it can never
   move the PLAY button -- that was the "breathing" bottom bar. */
function setHomeMsg(t){
  var el=document.getElementById("homeMsg"); if(el) el.textContent=t||"";
}
/* Every dynamic label goes through here, so a language switch repaints the
   whole UI in one call instead of leaving half the screen in the old language. */
function refreshStartChips(){ refreshLabels(); }
function refreshLabels(){
  var ac=document.getElementById("achCount"); if(ac) ac.textContent=achCount()+"/9";
  var hb=document.getElementById("homeBest"); if(hb) hb.textContent=store.best;
  var hm=document.getElementById("homeMelons"); if(hm) hm.textContent=store.melons;
  var tb=document.getElementById("themeBtn");
  if(tb) tb.textContent = store.theme==="classic"? T("desi") : T("classic");
  var db=document.getElementById("dailyBtn");
  if(db){ db.textContent = dailyMode? T("dailyOn") : T("dailyOff"); db.classList.toggle("on",dailyMode); }
  var lb=document.getElementById("luckyBtn");
  if(lb) lb.textContent = store.lastLucky===todayKey()? T("luckyDone") : T("lucky");
  var ag=document.getElementById("againBtn"); if(ag) ag.textContent=T("again");
  var h3=document.getElementById("homeBtn3"); if(h3) h3.textContent=T("homeScreen");
  var h2=document.getElementById("homeBtn2"); if(h2) h2.textContent=T("homeScreen");
  var rs=document.getElementById("resumeBtn"); if(rs) rs.textContent=T("resume");
  var cb=document.getElementById("continueBtn"); if(cb) cb.textContent=T("continueAd");
  var vm=document.getElementById("volMute"); if(vm) vm.textContent = muted? T("unmute") : T("mute");
  var et=document.getElementById("endTitle"); if(et&&state==="over") et.textContent=T("gameOver");
  buildAchGrid();
}

/* ---------- 13. lucky box ---------- */
/* The Lucky Box is a real prize wheel: every segment is a live prize, the
   pointer at the top lands on whichever one the spin chooses, and that exact
   prize is granted. One spin per day. */
var LUCKY_PRIZES=[
  {id:"sweep",   e:"🧹", t:"+1 Sweep",   c:"#ffd9a1", g:function(){ store.inv.sweep++; }},
  {id:"undo",    e:"↩",  t:"+1 Undo",    c:"#c9f0ff", g:function(){ store.inv.undo++; }},
  {id:"freeze",  e:"❄",  t:"+1 Freeze",  c:"#d8e9ff", g:function(){ store.inv.freeze++; }},
  {id:"bomb",    e:"💣", t:"+1 Bomb",    c:"#ffd0d0", g:function(){ store.inv.bomb++; }},
  {id:"dia",     e:"💎", t:"+25 Gems",   c:"#e3d0ff", g:function(){ addDiamonds(25,"Lucky Box"); }},
  {id:"golden",  e:"⭐", t:"Golden Drop",c:"#fff3b0", g:function(){ pendingBoost.push("golden"); }}
];
var luckySpin=0, luckySpinning=false;
function drawLuckyWheel(rot){
  var cv=document.getElementById("luckyWheel"); if(!cv||!cv.getContext) return;
  var x=cv.getContext("2d"), N=LUCKY_PRIZES.length, seg=Math.PI*2/N;
  var cx=140, cy=140, R=132;
  x.clearRect(0,0,280,280);
  for(var i=0;i<N;i++){
    var a0=rot+i*seg, a1=a0+seg;
    x.beginPath(); x.moveTo(cx,cy); x.arc(cx,cy,R,a0,a1); x.closePath();
    x.fillStyle=LUCKY_PRIZES[i].c; x.fill();
    x.lineWidth=3; x.strokeStyle="#fff"; x.stroke();
    var mid=a0+seg/2;
    x.save(); x.translate(cx,cy); x.rotate(mid);
    x.textAlign="right"; x.font="22px system-ui"; x.fillText(LUCKY_PRIZES[i].e, R-12, 8);
    x.restore();
  }
  x.beginPath(); x.arc(cx,cy,26,0,Math.PI*2); x.fillStyle="#fff"; x.fill();
  x.lineWidth=4; x.strokeStyle="#ffd93d"; x.stroke();
  x.textAlign="center"; x.font="20px system-ui"; x.fillText("🎁", cx, cy+7);
}
function grantLucky(pr){
  pr.g(); save(); updatePowerUI(); refreshEcon(); refreshStartChips();
  var el=document.getElementById("luckyResult");
  if(el) el.textContent="You won "+pr.e+" "+pr.t+"!";
  sfxUnlock(); buzz([30,30,30]);
}
function spinLucky(){
  if(luckySpinning) return;
  if(store.lastLucky===todayKey()) return;
  luckySpinning=true;
  var btn=document.getElementById("spinBtn"); if(btn) btn.disabled=true;
  var N=LUCKY_PRIZES.length, seg=Math.PI*2/N;
  var win=Math.floor(Math.random()*N);
  var turns=4+Math.floor(Math.random()*3);
  // pointer at top = -PI/2; land the winner's centre exactly under it
  var target=-Math.PI/2 - (win*seg+seg/2) + Math.PI*2*turns;
  var start=luckySpin, t0=performance.now(), dur=3400;
  function frame(t){
    var q=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-q,3);
    luckySpin=start+(target-start)*e;
    drawLuckyWheel(luckySpin);
    if(q<1){ requestAnimationFrame(frame); }
    else{
      luckySpinning=false;
      store.lastLucky=todayKey(); save(); refreshStartChips();
      grantLucky(LUCKY_PRIZES[win]);
      if(btn) btn.textContent="Come back tomorrow";
    }
  }
  requestAnimationFrame(frame);
}
document.getElementById("luckyBtn").addEventListener("click",function(){
  openPanel("luckyOv");
  drawLuckyWheel(luckySpin);
  var used=store.lastLucky===todayKey();
  var btn=document.getElementById("spinBtn");
  if(btn){ btn.disabled=used; btn.textContent= used? "Come back tomorrow":"🎡 SPIN"; }
  var res=document.getElementById("luckyResult");
  if(res) res.textContent= used? "Already spun today." : "Spin to win a prize!";
});
document.getElementById("spinBtn").addEventListener("click",spinLucky);
document.getElementById("luckyClose").addEventListener("click",function(){
  document.getElementById("luckyOv").classList.add("hide");
});
document.getElementById("themeBtn").addEventListener("click",function(){
  store.theme = store.theme==="classic"? "desi":"classic"; save(); refreshStartChips(); drawNext();
  document.getElementById("titleFruit").textContent = store.theme==="desi"? "🥭":"🍉";
});
document.getElementById("dailyBtn").addEventListener("click",function(){
  dailyMode=!dailyMode;
  if(dailyMode) store.lastDaily=todayKey(), save();
  refreshStartChips();
});
/* The old version dumped all nine achievements into a single-line <p> on the
   home screen, which grew to six lines and shoved the PLAY button around.
   They live in their own panel now. */
function buildAchGrid(){
  var g=document.getElementById("achGrid"); if(!g) return;
  var got=store.achGot||{};
  var html="", n=0;
  for(var k in ACH){
    var on=!!store.ach[k]; if(on) n++;
    var foot;
    if(on&&got[k]) foot='<div class="achGot">✔ +'+ACH[k].r+' 💎</div>';
    else if(on)    foot='<button class="achClaim" data-ach="'+k+'">+'+ACH[k].r+' 💎</button>';
    else           foot='<div class="achRew">+'+ACH[k].r+' 💎</div>';
    html+='<div class="achTile'+(on?" on":"")+'"><div class="achIco">'+ACH[k].i+
          '</div><div class="achName">'+achName(k)+'</div>'+foot+'</div>';
  }
  g.innerHTML=html;
  var f=document.getElementById("achFill"); if(f) f.style.width=Math.round(n/Object.keys(ACH).length*100)+"%";
  var sub=document.getElementById("achSub"); if(sub) sub.textContent=T("achUnlocked",n);
  var cnt=document.getElementById("achCount"); if(cnt) cnt.textContent=n+"/"+Object.keys(ACH).length;
}
document.getElementById("achBtn").addEventListener("click",function(){
  buildAchGrid();
  document.getElementById("achOv").classList.remove("hide");
  ac();
});
/* Claiming an achievement's diamonds. Delegation because the tiles are rebuilt
   from innerHTML each render. Once claimed, the button becomes a static "✔". */
function collectAch(k){
  if(!k||!store.ach[k]) return false;
  if(!store.achGot) store.achGot={};
  if(store.achGot[k]) return false;
  store.achGot[k]=true;
  addDiamonds(ACH[k].r,achName(k));
  sfxUnlock(); buzz(20);
  buildAchGrid();
  return true;
}
document.getElementById("achGrid").addEventListener("click",function(e){
  var t=e.target&&e.target.closest? e.target.closest(".achClaim") : null;
  if(t) collectAch(t.getAttribute("data-ach"));
});
document.getElementById("achClose").addEventListener("click",function(){
  document.getElementById("achOv").classList.add("hide");
});
document.getElementById("achOv").addEventListener("click",function(e){
  if(e.target===this) this.classList.add("hide");
});
