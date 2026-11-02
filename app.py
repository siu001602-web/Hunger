import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="20인 AI 헝거게임 & 경기장 맵",
    page_icon="🗺️",
    layout="wide"
)

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 헝거게임 시뮬레이터 & 맵</title>
  <style>
    :root {
      --bg-color: #0f172a;
      --panel-bg: #1e293b;
      --accent-color: #f59e0b;
      --text-main: #f8fafc;
      --border-color: #334155;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }
    body { background-color: var(--bg-color); color: var(--text-main); padding: 20px; display: flex; flex-direction: column; gap: 20px; }

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
    .btn:disabled { opacity: 0.4; cursor: not-allowed; }

    .game-status-bar {
      display: flex; gap: 20px; background-color: var(--panel-bg); padding: 12px 20px; border-radius: 12px; border: 1px solid var(--border-color);
    }

    .main-layout {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 20px;
    }
    @media (max-width: 1200px) {
      .main-layout { grid-template-columns: 1fr; }
    }

    /* 맵 스타일 */
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
    }

    .sector-center { background-color: #7c2d12; color: #ffedd5; } /* 중앙 풍요의 뿔 */
    .sector-forest { background-color: #14532d; color: #dcfce7; } /* 숲 지대 */
    .sector-mountain { background-color: #3f3f46; color: #f4f4f5; } /* 산악 지대 */
    .sector-lake { background-color: #0c4a6e; color: #e0f2fe; } /* 호수/강 */
    .sector-ruins { background-color: #4c1d95; color: #f3e8ff; } /* 폐허 */

    .sector-title { font-weight: bold; opacity: 0.8; font-size: 0.7rem; }
    .player-tokens { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
    .token {
      background: #2563eb;
      color: white;
      font-size: 0.65rem;
      padding: 2px 4px;
      border-radius: 4px;
      font-weight: bold;
      box-shadow: 0 0 4px rgba(0,0,0,0.5);
    }
    .token-dead { background: #475569; opacity: 0.5; text-decoration: line-through; }

    /* 플레이어 리스트 및 로그 */
    .grid-players { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; max-height: 500px; overflow-y: auto; }
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
    .log-move { border-left: 3px solid #10b981; color: #a7f3d0; }
  </style>
</head>
<body>

  <header>
    <h1>🗺️ 20인 헝거게임 경기장 맵 시뮬레이터</h1>
    <button class="btn btn-primary" onclick="initGame()">새 경기 시작</button>
  </header>

  <div class="game-status-bar">
    <div>라운드: <span id="round-count">1</span></div>
    <div>생존자: <span id="alive-count">20</span> / 20명</div>
  </div>

  <div class="main-layout">
    <!-- 1. 경기장 맵 시각화 -->
    <div class="map-container">
      <h3>🗺️ 경기장 구역 맵 (4x4)</h3>
      <div class="arena-grid" id="arena-map"></div>
    </div>

    <!-- 2. 참가자 현황 -->
    <div>
      <h3>👥 참가자 상태 현황</h3>
      <br>
      <div class="grid-players" id="player-grid"></div>
    </div>

    <!-- 3. 경기 진행 로그 -->
    <div class="log-container">
      <h3>📜 라운드 진행 로그</h3>
      <div class="log-messages" id="log-box"></div>
      <div style="margin-top: 10px;">
        <button class="btn btn-warning" id="btn-next" onclick="nextRound()">⚔️ 다음 라운드 진행</button>
      </div>
    </div>
  </div>

  <script>
    const TOTAL = 20;
    const NAMES = ["카트니스", "피타", "게일", "헤이밋치", "피닉", "조한나", "루", "카토", "클로브", "마블",
                   "글리머", "트레시", "포스포어", "브루투스", "에노바리아", "비티", "바이퍼", "오마르", "엘리", "잭"];
    
    // 4x4 구역 정보 정의
    const SECTORS = [
      { id: 0, name: "북서쪽 산악", type: "mountain" },
      { id: 1, name: "북쪽 숲", type: "forest" },
      { id: 2, name: "북동쪽 숲", type: "forest" },
      { id: 3, name: "동쪽 호수", type: "lake" },
      { id: 4, name: "서쪽 숲", type: "forest" },
      { id: 5, name: "풍요의 뿔(중앙)", type: "center" },
      { id: 6, name: "풍요의 뿔(중앙)", type: "center" },
      { id: 7, name: "동쪽 숲", type: "forest" },
      { id: 8, name: "서쪽 폐허", type: "ruins" },
      { id: 9, name: "남서쪽 숲", type: "forest" },
      { id: 10, name: "남쪽 호수", type: "lake" },
      { id: 11, name: "남동쪽 산악", type: "mountain" },
      { id: 12, name: "남서쪽 절벽", type: "mountain" },
      { id: 13, name: "남쪽 숲", type: "forest" },
      { id: 14, name: "남동쪽 숲", type: "forest" },
      { id: 15, name: "동남쪽 폐허", type: "ruins" }
    ];

    const WEAPONS = [
      { name: "맨손", dmg: 10 },
      { name: "돌멩이", dmg: 15 },
      { name: "단검", dmg: 25 },
      { name: "장궁", dmg: 35 },
      { name: "강철 창", dmg: 45 }
    ];

    let players = [];
    let round = 1;

    function log(msg, type = 'event') {
      const box = document.getElementById('log-box');
      const div = document.createElement('div');
      div.className = `log-item log-${type}`;
      div.innerHTML = msg;
      box.appendChild(div);
      box.scrollTop = box.scrollHeight;
    }

    function initGame() {
      players = Array.from({length: TOTAL}, (_, i) => ({
        id: i + 1,
        name: NAMES[i],
        hp: 100,
        weapon: WEAPONS[0],
        sectorId: (i % 2 === 0) ? 5 : 6, // 게임 시작 시 중앙(풍요의 뿔)에 스폰
        isAlive: true
      }));

      round = 1;
      document.getElementById('log-box').innerHTML = '';
      log(`🚩 경기 시작! 모든 참가자가 <strong>풍요의 뿔 광장</strong>에 모였습니다!`, 'event');
      updateUI();
    }

    function updateUI() {
      // 1. 맵 UI 업데이트
      const mapGrid = document.getElementById('arena-map');
      mapGrid.innerHTML = '';

      SECTORS.forEach(sec => {
        const secDiv = document.createElement('div');
        secDiv.className = `sector sector-${sec.type}`;
        
        const inSectorPlayers = players.filter(p => p.sectorId === sec.id && p.isAlive);
        let tokensHtml = inSectorPlayers.map(p => `<span class="token">${p.name}</span>`).join('');

        secDiv.innerHTML = `
          <div class="sector-title">${sec.name}</div>
          <div class="player-tokens">${tokensHtml}</div>
        `;
        mapGrid.appendChild(secDiv);
      });

      // 2. 플레이어 카드 UI 업데이트
      const playerGrid = document.getElementById('player-grid');
      playerGrid.innerHTML = '';
      let aliveCnt = 0;

      players.forEach(p => {
        if (p.isAlive) aliveCnt++;
        const card = document.createElement('div');
        card.className = `player-card ${p.isAlive ? '' : 'dead'}`;

        const sectorName = SECTORS[p.sectorId].name;

        card.innerHTML = `
          <strong>${p.name}</strong><br>
          <span style="font-size:0.7rem; color:#60a5fa;">📍 ${sectorName}</span><br>
          <span style="font-size:0.7rem;">🗡️ ${p.weapon.name}</span>
          <div class="hp-bar-bg">
            <div class="hp-bar-fill" style="width: ${Math.max(0, p.hp)}%;"></div>
          </div>
          <span style="font-size:0.7rem;">HP: ${Math.max(0, p.hp)}</span>
        `;
        playerGrid.appendChild(card);
      });

      document.getElementById('alive-count').innerText = aliveCnt;
      document.getElementById('round-count').innerText = round;

      if (aliveCnt <= 1) {
        document.getElementById('btn-next').disabled = true;
      } else {
        document.getElementById('btn-next').disabled = false;
      }
    }

    function nextRound() {
      const aliveList = players.filter(p => p.isAlive);
      if (aliveList.length <= 1) return;

      log(`--- 📢 라운드 ${round} 진행 ---`, 'event');

      // 1. 플레이어 이동 처리
      aliveList.forEach(p => {
        if (Math.random() < 0.6) { // 60% 확률로 다른 위치 이동
          const newSector = Math.floor(Math.random() * SECTORS.length);
          p.sectorId = newSector;
        }
      });

      // 2. 파밍/무기 획득 이벤트
      const luckyPlayer = aliveList[Math.floor(Math.random() * aliveList.length)];
      const newWep = WEAPONS[Math.floor(Math.random() * (WEAPONS.length - 1)) + 1];
      if (newWep.dmg > luckyPlayer.weapon.dmg) {
        luckyPlayer.weapon = newWep;
        log(`🎒 <strong>${luckyPlayer.name}</strong>이(가) [${SECTORS[luckyPlayer.sectorId].name}]에서 [${newWep.name}]을(를) 주웠습니다!`, 'move');
      }

      // 3. 같은 구역(섹터)에 있는 플레이어들끼리 전투 교전
      SECTORS.forEach(sec => {
        const secAlive = players.filter(p => p.sectorId === sec.id && p.isAlive);
        if (secAlive.length >= 2) {
          // 2명 선택 후 교전
          const p1 = secAlive[0];
          const p2 = secAlive[1];

          const damage = p1.weapon.dmg + Math.floor(Math.random() * 10);
          p2.hp -= damage;

          log(`⚔️ [${sec.name}] <strong>${p1.name}</strong>이(가) ${p1.weapon.name}(으)로 <strong>${p2.name}</strong>을(를) 공격해 ${damage} 피해!`, 'battle');

          if (p2.hp <= 0) {
            p2.isAlive = false;
            p2.hp = 0;
            log(`💀 <strong>${p2.name}</strong>이(가) [${sec.name}]에서 사망하였습니다!`, 'battle');
          }
        }
      });

      // 승리 판정
      const currentAlive = players.filter(p => p.isAlive);
      if (currentAlive.length === 1) {
        log(`🏆 <strong>경기 종료! ${currentAlive[0].name}이(가) 최종 최후의 1인으로 우승하였습니다!</strong>`, 'event');
      }

      round++;
      updateUI();
    }

    window.onload = initGame;
  </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
