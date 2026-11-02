import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="헝거게임 - 구역 봉쇄 & 풀피 회복 시스템",
    page_icon="🔥",
    layout="wide"
)

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>헝거게임 시뮬레이터</title>
  <style>
    :root {
      --bg-color: #0f172a;
      --panel-bg: #1e293b;
      --accent-color: #f59e0b;
      --text-main: #f8fafc;
      --border-color: #334155;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }
    body { background-color: var(--bg-color); color: var(--text-main); padding: 20px; display: flex; flex-direction: column; gap: 20px; position: relative; }

    header {
      background-color: var(--panel-bg);
      padding: 15px 20px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }

    .btn {
      padding: 8px 16px; border-radius: 6px; border: none; font-weight: bold; cursor: pointer; transition: 0.2s;
    }
    .btn-primary { background-color: #2563eb; color: white; }
    .btn-warning { background-color: #d97706; color: white; }
    .btn-danger { background-color: #e11d48; color: white; }
    .btn:disabled { opacity: 0.4; cursor: not-allowed; }

    .game-status-bar {
      display: flex; gap: 20px; background-color: var(--panel-bg); padding: 12px 20px; border-radius: 12px; border: 1px solid var(--border-color);
      align-items: center; font-size: 1.1rem; flex-wrap: wrap;
    }

    .main-layout {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 20px;
    }
    @media (max-width: 1200px) {
      .main-layout { grid-template-columns: 1fr; }
    }

    .map-container {
      background-color: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 15px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .arena-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: repeat(4, 1fr);
      gap: 6px;
      aspect-ratio: 1 / 1;
      background-color: #020617;
      padding: 8px;
      border-radius: 8px;
      border: 2px solid var(--border-color);
    }

    .sector {
      border: 1px dashed #475569;
      border-radius: 6px;
      padding: 6px;
      font-size: 0.75rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      transition: background-color 0.3s;
    }

    .sector-center { background-color: #7c2d12; color: #ffedd5; }
    .sector-forest { background-color: #14532d; color: #dcfce7; }
    .sector-mountain { background-color: #3f3f46; color: #f4f4f5; }
    .sector-lake { background-color: #0c4a6e; color: #e0f2fe; }
    .sector-ruins { background-color: #4c1d95; color: #f3e8ff; }

    /* 구역 봉쇄 시 스타일 */
    .sector.sealed {
      background-color: #450a0a !important;
      border: 2px solid #ef4444 !important;
      color: #fca5a5;
    }

    .sector-title { font-weight: bold; opacity: 0.8; font-size: 0.65rem; }
    .player-tokens { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 3px; }
    .token {
      font-size: 0.6rem;
      padding: 2px 4px;
      border-radius: 3px;
      font-weight: bold;
    }

    .grid-players { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; max-height: 500px; overflow-y: auto; }
    .player-card {
      background-color: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 8px; text-align: center;
    }
    .player-card.dead { opacity: 0.3; background-color: #111; }

    .hp-bar-bg { background: #334155; border-radius: 4px; height: 6px; margin-top: 4px; overflow: hidden; }
    .hp-bar-fill { background: #22c55e; height: 100%; transition: width 0.3s; }

    .log-container {
      background-color: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px;
      display: flex; flex-direction: column; height: 550px;
    }
    .log-messages { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
    .log-item { padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; background: #0f172a; line-height: 1.4; }
    .log-event { border-left: 3px solid #f59e0b; }
    .log-battle { border-left: 3px solid #ef4444; color: #fca5a5; }
    .log-team { border-left: 3px solid #3b82f6; color: #bfdbfe; }
    .log-betray { border-left: 3px solid #a855f7; color: #f3e8ff; }
    .log-seal { border-left: 3px solid #dc2626; color: #fecaca; font-weight: bold; }

    #death-modal {
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.75); display: flex; justify-content: center; align-items: center;
      z-index: 9999; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
    }
    #death-modal.show { opacity: 1; pointer-events: auto; }
    .modal-content {
      background: #7f1d1d; border: 3px solid #f87171; padding: 30px 50px; border-radius: 16px;
      text-align: center; box-shadow: 0 0 30px rgba(239, 68, 68, 0.6);
      animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes popIn {
      0% { transform: scale(0.6); }
      100% { transform: scale(1); }
    }
  </style>
</head>
<body>

  <div id="death-modal">
    <div class="modal-content">
      <h2 style="color: #fca5a5; font-size: 1.8rem; margin-bottom: 10px;">💀 사망 발생!</h2>
      <p id="death-modal-text" style="font-size: 1.2rem; font-weight: bold; color: #fff;">누군가 사망했습니다.</p>
    </div>
  </div>

  <header>
    <h1>🔥 헝거게임 (구역봉쇄 & 풀피회복 시스템)</h1>
    <div style="display: flex; gap: 10px;">
      <button class="btn btn-primary" onclick="initGame()">새 경기 시작</button>
      <button class="btn btn-warning" id="btn-auto" onclick="toggleAutoPlay()">⏰ 자동 진행 시작 (10초)</button>
    </div>
  </header>

  <div class="game-status-bar">
    <div>라운드: <span id="round-count">1</span></div>
    <div>생존자: <span id="alive-count">20</span> / 20명</div>
    <div>다음 구역 봉쇄까지: <span id="seal-countdown" style="color: #f59e0b; font-weight: bold;">10</span>턴 남음</div>
    <div>상태: <span id="auto-status" style="color: #4ade80; font-weight: bold;">수동 조작 중</span></div>
  </div>

  <div class="main-layout">
    <div class="map-container">
      <h3>🗺️ 경기장 맵 (4x4)</h3>
      <div class="arena-grid" id="arena-map"></div>
    </div>

    <div>
      <h3>👥 참가자 상태 현황</h3>
      <br>
      <div class="grid-players" id="player-grid"></div>
    </div>

    <div class="log-container">
      <h3>📜 경기 진행 로그</h3>
      <div class="log-messages" id="log-box"></div>
      <div style="margin-top: 10px;">
        <button class="btn btn-warning" id="btn-next" onclick="nextRound()" style="width: 100%;">⚔️ 수동 다음 라운드</button>
      </div>
    </div>
  </div>

  <script>
    const TOTAL = 20;
    const NAMES = ["카트니스", "피타", "게일", "헤이밋치", "피닉", "조한나", "루", "카토", "클로브", "마블",
                   "글리머", "트레시", "포스포어", "브루투스", "에노바리아", "비티", "바이퍼", "오마르", "엘리", "잭"];
    
    const SECTORS = [
      { id: 0, name: "북서 산악", type: "mountain" }, { id: 1, name: "북쪽 숲", type: "forest" },
      { id: 2, name: "북동 숲", type: "forest" }, { id: 3, name: "동쪽 호수", type: "lake" },
      { id: 4, name: "서쪽 숲", type: "forest" }, { id: 5, name: "풍요의 뿔", type: "center" },
      { id: 6, name: "풍요의 뿔", type: "center" }, { id: 7, name: "동쪽 숲", type: "forest" },
      { id: 8, name: "서쪽 폐허", type: "ruins" }, { id: 9, name: "남서 숲", type: "forest" },
      { id: 10, name: "남쪽 호수", type: "lake" }, { id: 11, name: "남동 산악", type: "mountain" },
      { id: 12, name: "남서 절벽", type: "mountain" }, { id: 13, name: "남쪽 숲", type: "forest" },
      { id: 14, name: "남동 숲", type: "forest" }, { id: 15, name: "동남 폐허", type: "ruins" }
    ];

    const WEAPONS_POOL = [
      { name: "돌멩이", dmg: 15 },
      { name: "단검", dmg: 25 },
      { name: "장궁", dmg: 35 },
      { name: "강철 창", dmg: 45 }
    ];

    let players = [];
    let round = 1;
    let sealedSectors = []; // 봉쇄된 구역 ID 목록
    let autoInterval = null;
    let isAutoRunning = false;

    function getPlayerColor(kills) {
      if (kills >= 5) return { color: "#ef4444", glow: "text-shadow: 0 0 6px #ef4444;" };
      if (kills >= 3) return { color: "#f59e0b", glow: "text-shadow: 0 0 4px #f59e0b;" };
      if (kills >= 1) return { color: "#38bdf8", glow: "" };
      return { color: "#f8fafc", glow: "" };
    }

    function log(msg, type = 'event') {
      const box = document.getElementById('log-box');
      const div = document.createElement('div');
      div.className = `log-item log-${type}`;
      div.innerHTML = msg;
      box.appendChild(div);
      box.scrollTop = box.scrollHeight;
    }

    function showDeathModal(text) {
      const modal = document.getElementById('death-modal');
      document.getElementById('death-modal-text').innerHTML = text;
      modal.classList.add('show');
      setTimeout(() => {
        modal.classList.remove('show');
      }, 2500);
    }

    function initGame() {
      stopAutoPlay();
      players = Array.from({length: TOTAL}, (_, i) => ({
        id: i + 1,
        name: NAMES[i],
        hp: 100,
        inventory: [],
        kills: 0,
        team: null,
        sectorId: (i % 2 === 0) ? 5 : 6,
        isAlive: true
      }));

      round = 1;
      sealedSectors = [];
      document.getElementById('log-box').innerHTML = '';
      log(`🚩 경기 시작! 20명의 참가자가 풍요의 뿔에 입장했습니다. (10턴마다 구역 봉쇄 발동)`, 'event');
      updateUI();
    }

    function toggleAutoPlay() {
      if (isAutoRunning) {
        stopAutoPlay();
      } else {
        startAutoPlay();
      }
    }

    function startAutoPlay() {
      isAutoRunning = true;
      document.getElementById('btn-auto').innerText = "⏹️ 자동 진행 중지";
      document.getElementById('btn-auto').style.backgroundColor = "#e11d48";
      document.getElementById('auto-status').innerText = "10초마다 자동 진행 중...";
      document.getElementById('auto-status').style.color = "#f59e0b";
      document.getElementById('btn-next').disabled = true;

      autoInterval = setInterval(() => {
        const alive = players.filter(p => p.isAlive);
        if (alive.length <= 1) {
          stopAutoPlay();
          return;
        }
        nextRound();
      }, 10000);
    }

    function stopAutoPlay() {
      isAutoRunning = false;
      document.getElementById('btn-auto').innerText = "⏰ 자동 진행 시작 (10초)";
      document.getElementById('btn-auto').style.backgroundColor = "#d97706";
      document.getElementById('auto-status').innerText = "수동 조작 중";
      document.getElementById('auto-status').style.color = "#4ade80";
      const aliveCount = players.filter(p => p.isAlive).length;
      if (aliveCount > 1) {
        document.getElementById('btn-next').disabled = false;
      }
      if (autoInterval) clearInterval(autoInterval);
    }

    function updateUI() {
      // 카운트다운 계산 (10턴 주기)
      const turnsLeft = 10 - ((round - 1) % 10);
      document.getElementById('seal-countdown').innerText = turnsLeft;

      const mapGrid = document.getElementById('arena-map');
      mapGrid.innerHTML = '';

      SECTORS.forEach(sec => {
        const secDiv = document.createElement('div');
        const isSealed = sealedSectors.includes(sec.id);
        secDiv.className = `sector sector-${sec.type} ${isSealed ? 'sealed' : ''}`;
        
        const inSec = players.filter(p => p.sectorId === sec.id && p.isAlive);
        let tokensHtml = inSec.map(p => {
          const style = getPlayerColor(p.kills);
          return `<span class="token" style="background:${style.color}; color:#0f172a;">${p.name} (${p.kills}킬)</span>`;
        }).join('');

        const sealLabel = isSealed ? '<div style="color:#f87171; font-weight:bold; font-size:0.6rem;">🚫 [봉쇄됨]</div>' : '';

        secDiv.innerHTML = `
          <div>
            <div class="sector-title">${sec.name}</div>
            ${sealLabel}
          </div>
          <div class="player-tokens">${tokensHtml}</div>
        `;
        mapGrid.appendChild(secDiv);
      });

      const playerGrid = document.getElementById('player-grid');
      playerGrid.innerHTML = '';
      let aliveCnt = 0;

      players.forEach(p => {
        if (p.isAlive) aliveCnt++;
        const card = document.createElement('div');
        card.className = `player-card ${p.isAlive ? '' : 'dead'}`;
        const teamBadge = p.team ? `<span style="color:#60a5fa; font-size:0.6rem;">[팀: ${p.team}]</span>` : `<span style="color:#94a3b8; font-size:0.6rem;">[솔로]</span>`;
        
        const style = getPlayerColor(p.kills);
        const invText = p.inventory.length > 0 ? p.inventory.map(w => w.name).join(', ') : '없음 (맨손)';

        card.innerHTML = `
          <strong style="color: ${style.color}; ${style.glow}">${p.name}</strong><br>
          ${teamBadge}<br>
          <span style="font-size:0.6rem; color:#f59e0b; font-weight:bold;">🎯 킬: ${p.kills}</span><br>
          <span style="font-size:0.6rem; color:#cbd5e1;">🎒 인벤: [${invText}]</span>
          <div class="hp-bar-bg">
            <div class="hp-bar-fill" style="width: ${Math.max(0, p.hp)}%; background: ${p.hp > 50 ? '#22c55e' : '#ef4444'};"></div>
          </div>
          <span style="font-size:0.6rem;">HP: ${Math.max(0, p.hp)}</span>
        `;
        playerGrid.appendChild(card);
      });

      document.getElementById('alive-count').innerText = aliveCnt;
      document.getElementById('round-count').innerText = round;

      if (aliveCnt <= 1 && isAutoRunning) {
        stopAutoPlay();
      }
    }

    function nextRound() {
      const aliveList = players.filter(p => p.isAlive);
      if (aliveList.length <= 1) return;

      log(`--- 📢 라운드 ${round} 시작 ---`, 'event');

      // 10턴마다 구역 봉쇄 이벤트 발동
      if (round > 1 && (round - 1) % 10 === 0) {
        // 아직 봉쇄되지 않은 구역 중 무작위 1개 선택
        const availableSectors = SECTORS.filter(sec => !sealedSectors.includes(sec.id));
        if (availableSectors.length > 0) {
          const targetSec = availableSectors[Math.floor(Math.random() * availableSectors.length)];
          sealedSectors.push(targetSec.id);

          log(`🚨 <strong>[구역 봉쇄 경보]</strong> 게임 주최측에 의해 <strong>[${targetSec.name}]</strong> 구역이 완전히 봉쇄되었습니다!`, 'seal');
          showDeathModal(`🚨 [구역 봉쇄]<br>${targetSec.name} 구역 폐쇄!`);

          // 해당 구역에 있던 생존자들 전멸 처리
          players.forEach(p => {
            if (p.isAlive && p.sectorId === targetSec.id) {
              p.isAlive = false;
              p.hp = 0;
              log(`💀 <strong>${p.name}</strong>님이 봉쇄된 [${targetsecName = targetSec.name}] 구역을 탈출하지 못해 사망했습니다!`, 'seal');
            }
          });
        }
      }

      // 1. 이동 (봉쇄된 구역으로는 이동하지 않도록 필터링)
      aliveList.forEach(p => {
        if (Math.random() < 0.65) {
          let availableMoves = SECTORS.filter(sec => !sealedSectors.includes(sec.id));
          if (availableMoves.length > 0) {
            const nextSec = availableMoves[Math.floor(Math.random() * availableMoves.length)];
            p.sectorId = nextSec.id;
          }
        }
      });

      // 2. 동맹 & 배신 이벤트
      if (Math.random() < 0.4) {
        const p1 = aliveList[Math.floor(Math.random() * aliveList.length)];
        const p2 = aliveList[Math.floor(Math.random() * aliveList.length)];
        if (p1.id !== p2.id) {
          if (p1.team && p1.team === p2.team && Math.random() < 0.3) {
            p1.team = null;
            log(`⚡ <strong>${p1.name}</strong>이(가) 팀원이었던 <strong>${p2.name}</strong>을(를) <strong>배신</strong>하고 이탈했습니다!`, 'betray');
          } else if (!p1.team && !p2.team) {
            const teamName = `팀-${p1.name.slice(0,1)}${p2.name.slice(0,1)}`;
            p1.team = teamName;
            p2.team = teamName;
            log(`🤝 <strong>${p1.name}</strong>와(과) <strong>${p2.name}</strong>이(가) 동맹 [${teamName}]을 결성했습니다!`, 'team');
          }
        }
      }

      // 3. 일회용 무기 파밍
      const lucky = aliveList[Math.floor(Math.random() * aliveList.length)];
      const foundWeapon = WEAPONS_POOL[Math.floor(Math.random() * WEAPONS_POOL.length)];
      lucky.inventory.push(foundWeapon);
      log(`🎁 <strong>${lucky.name}</strong>이(가) [${SECTORS[lucky.sectorId].name}]에서 일회용 무기 [${foundWeapon.name}](공격력 ${foundWeapon.dmg})을(를) 주워 가방에 넣었습니다!`, 'event');

      // 4. 전투 및 일회용 무기 소모 시스템
      SECTORS.forEach(sec => {
        // 봉쇄된 구역에서는 전투 발생 안 함
        if (sealedSectors.includes(sec.id)) return;

        const secAlive = players.filter(p => p.sectorId === sec.id && p.isAlive);
        if (secAlive.length >= 2) {
          const p1 = secAlive[0];
          const enemies = secAlive.filter(p => p.id !== p1.id && (!p1.team || p1.team !== p.team));
          const targetPool = enemies.length > 0 ? enemies : secAlive.filter(p => p.id !== p1.id);
          
          if (targetPool.length > 0) {
            const p2 = targetPool[Math.floor(Math.random() * targetPool.length)];

            let usedWeaponName = "맨손";
            let baseDmg = 10;

            if (p1.inventory.length > 0) {
              p1.inventory.sort((a, b) => b.dmg - a.dmg);
              const consumedWeapon = p1.inventory.shift();
              usedWeaponName = consumedWeapon.name;
              baseDmg = consumedWeapon.dmg;
            }

            const dmg = baseDmg + Math.floor(Math.random() * 10);
            p2.hp -= dmg;

            log(`⚔️ [${sec.name}] <strong>${p1.name}</strong>이(가) <strong>[${usedWeaponName}]</strong>을(를) 사용하여 <strong>${p2.name}</strong>을(를) 공격! (${dmg} 피해)`, 'battle');

            if (p2.hp <= 0 && p2.isAlive) {
              p2.isAlive = false;
              p2.hp = 0;
              p1.kills += 1;
              
              // [추가 규칙] 사람을 죽이면 본인 체력이 풀피(100)로 회복!
              p1.hp = 100;

              showDeathModal(`<strong>${p2.name}</strong>님이 전사했습니다!<br><span style="color:#f59e0b; font-size:1rem;">(처치자: ${p1.name} / 총 ${p1.kills}킬 / HP 풀피 회복!)</span>`);
              log(`💀 <strong>${p2.name}</strong>이(가) 전사했습니다! <span style="color:#f59e0b;">(🔥 ${p1.name} 킬수 +1 [총 ${p1.kills}킬] & <strong>체력 완전 회복!</strong>)</span>`, 'battle');
            }
          }
        }
      });

      const currentAlive = players.filter(p => p.isAlive);
      if (currentAlive.length === 1) {
        log(`🏆 <strong>최종 우승자: ${currentAlive[0].name} (총 ${currentAlive[0].kills}킬)!!</strong>`, 'event');
        stopAutoPlay();
      }

      round++;
      updateUI();
    }

    window.onload = initGame;
  </script>
</body>
</html>
"""

components.html(html_code, height=920, scrolling=True)
