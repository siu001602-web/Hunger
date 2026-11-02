import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI 헝거게임 시뮬레이터",
    page_icon="🏹",
    layout="wide"
)

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 헝거게임 시뮬레이터</title>
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

    .main-content { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
    @media (max-width: 1024px) { .main-content { grid-template-columns: 1fr; } }

    .grid-players { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; }
    .player-card {
      background-color: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; text-align: center;
    }
    .player-card.dead { opacity: 0.3; background-color: #111; }

    .hp-bar-bg { background: #334155; border-radius: 4px; height: 8px; margin-top: 6px; overflow: hidden; }
    .hp-bar-fill { background: #22c55e; height: 100%; transition: width 0.3s; }

    .log-container {
      background-color: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px;
      display: flex; flex-direction: column; height: 600px;
    }
    .log-messages { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
    .log-item { padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; background: #0f172a; line-height: 1.4; }
    .log-event { border-left: 3px solid #f59e0b; }
    .log-battle { border-left: 3px solid #ef4444; color: #fca5a5; }
    .log-team { border-left: 3px solid #3b82f6; color: #bfdbfe; }
  </style>
</head>
<body>

  <header>
    <h1>🏹 20인 AI 헝거게임 시뮬레이터</h1>
    <button class="btn btn-primary" onclick="initGame()">새 경기 시작</button>
  </header>

  <div class="game-status-bar">
    <div>라운드: <span id="round-count">1</span></div>
    <div>생존자: <span id="alive-count">20</span> / 20명</div>
  </div>

  <div class="main-content">
    <div>
      <h3>참가자 현황</h3>
      <br>
      <div class="grid-players" id="player-grid"></div>
    </div>

    <div class="log-container">
      <h3>경기 진행 로그</h3>
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
    const WEAPONS = [
      { name: "맨손", dmg: 5 },
      { name: "돌멩이", dmg: 10 },
      { name: "단검", dmg: 20 },
      { name: "장궁", dmg: 35 },
      { name: "강철 창", dmg: 40 },
      { name: "장검", dmg: 45 }
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
        teamId: null,
        isAlive: true
      }));

      round = 1;
      document.getElementById('log-box').innerHTML = '';
      log(`🚩 20명의 참가자가 경기장에 입장했습니다! 모든 플레이어 HP: 100`, 'event');
      updateUI();
    }

    function updateUI() {
      const grid = document.getElementById('player-grid');
      grid.innerHTML = '';
      let aliveCnt = 0;

      players.forEach(p => {
        if (p.isAlive) aliveCnt++;
        const card = document.createElement('div');
        card.className = `player-card ${p.isAlive ? '' : 'dead'}`;

        const hpPercent = Math.max(0, p.hp);
        const teamText = p.teamId ? `[팀 ${p.teamId}]` : '단독';

        card.innerHTML = `
          <strong>${p.name}</strong><br>
          <span style="font-size:0.75rem; color:#94a3b8;">${teamText}</span><br>
          <span style="font-size:0.75rem;">🗡️ ${p.weapon.name}</span>
          <div class="hp-bar-bg">
            <div class="hp-bar-fill" style="width: ${hpPercent}%;"></div>
          </div>
          <span style="font-size:0.75rem;">HP: ${Math.max(0, p.hp)}</span>
        `;
        grid.appendChild(card);
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

      log(`--- 📢 라운드 ${round} 시작 ---`, 'event');

      // 1. 무기 수집 이벤트
      if (Math.random() < 0.4) {
        const p = aliveList[Math.floor(Math.random() * aliveList.length)];
        const newWep = WEAPONS[Math.floor(Math.random() * (WEAPONS.length - 1)) + 1];
        if (newWep.dmg > p.weapon.dmg) {
          p.weapon = newWep;
          log(`🎁 <strong>${p.name}</strong>이(가) 상자를 발견하여 [${newWep.name}](공격력 ${newWep.dmg})을(를) 획득했습니다!`, 'event');
        }
      }

      // 2. 동맹 결성 이벤트
      if (Math.random() < 0.3) {
        const noTeam = aliveList.filter(p => !p.teamId);
        if (noTeam.length >= 2) {
          const p1 = noTeam[0];
          const p2 = noTeam[1];
          const newTeamId = Math.floor(Math.random() * 100) + 1;
          p1.teamId = newTeamId;
          p2.teamId = newTeamId;
          log(`🤝 <strong>${p1.name}</strong>와(과) <strong>${p2.name}</strong>이(가) 생존을 위해 동맹을 맺었습니다!`, 'team');
        }
      }

      // 3. 전투 발생
      const p1 = aliveList[Math.floor(Math.random() * aliveList.length)];
      // 자신이나 같은 팀원 제외한 타겟 선정
      const targets = aliveList.filter(p => p.id !== p1.id && (p.teamId === null || p.teamId !== p1.teamId));

      if (targets.length > 0) {
        const p2 = targets[Math.floor(Math.random() * targets.length)];
        const damage = p1.weapon.dmg + Math.floor(Math.random() * 10);
        p2.hp -= damage;

        log(`⚔️ <strong>${p1.name}</strong>이(가) ${p1.weapon.name}(으)로 <strong>${p2.name}</strong>을(를) 공격해 ${damage} 피해를 입혔습니다!`, 'battle');

        if (p2.hp <= 0) {
          p2.isAlive = false;
          p2.hp = 0;
          log(`💀 <strong>${p2.name}</strong>이(가) 치명상을 입고 탈락했습니다!`, 'battle');
        }
      }

      // 승리 조건 체크
      const currentAlive = players.filter(p => p.isAlive);
      if (currentAlive.length === 1) {
        log(`🏆 <strong>축하합니다! ${currentAlive[0].name}이(가) 헝거게임의 최종 우승자가 되었습니다!</strong>`, 'event');
      }

      round++;
      updateUI();
    }

    window.onload = initGame;
  </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
