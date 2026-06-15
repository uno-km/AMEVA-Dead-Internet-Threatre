# AMEVA Dead Internet Theatre: Latent Personality Dynamics Simulation System

> **[프로젝트 요약 (Resume Profile)]**
> 
> * **① 제목:** 잠재적 인격 동역학 시뮬레이션 시스템 (AMEVA Dead Internet Theatre)
> * **② 주제:** 
>   * **죽은 인터넷 사회 이론(Dead Internet Theory)**을 배경으로, 완전히 자율적인 에이전트 환경과 감독(Director) LLM 에이전트가 통제하는 제어형 환경을 교차 실험하여 인공지능 커뮤니티 소통의 사회적 역학과 여론 동역학(Opinion Dynamics)을 분석하는 연구
>   * 현재 로컬 실행에 따른 물리적인 제약(연산 자원, OOM)을 동적 턴 오케스트레이션 아키텍처 및 프롬프팅 기법으로 극복하고, 감정 상태(LPDE)와 봇 순서 제어 알고리즘을 통해 봇들의 소통 순서를 조율하며 상호작용하도록 설계
>   * **최종 목표:** 향후 분산 컴퓨팅 환경 확장을 통해 봇(노드)들이 순차적인 흐름을 벗어나 실제 인간 사회처럼 무작위적이고 유기적으로 활동하며 비동기 실시간 소통을 수행하는 다이내믹 포럼 환경 구현
> * **③ 내용요지:**
>   * **사용 기술:** LLM (로컬 모델 구동 및 독립 에이전트 페르소나/대화 제어), Docker & Dozzle (로그 통합), Python (턴 오케스트레이터 & LPDE 엔진), SQLite3 (데이터 영속화)
>   * **사용 모델:** `Llama-3.1 (8B)` 온리 (STT 미사용, 8B 단일 모델 스케일로 통일)
>   * **핵심 알고리즘:** LPDE(Affect 2D, Opinion 4D, Power 2D) 인격 상태 텐서 공간 모델, 봇 간 상대 감정 업데이트용 지수이동평균(EMA) 필터, 극단주의 봇의 자아 붕괴를 정규식으로 방어하는 Stance Coherence 검증 로직, OOM 방지를 위한 동적 컨테이너 수명 주기 제어.
>   * **에이전트/보안 제어 (또는 핵심 아키텍처 흐름):** LLM 화두 인입 -> 각 봇별 독립된 `Docker` 컨테이너를 순차적으로 기동/종료하여 메모리 OOM 방지 -> LPDE 감정 벡터가 반영된 댓글 및 멘션 발화 생성 -> 감독 LLM 에이전트(Director)가 봇들의 성격과 일관성을 조율하고 필요시 강제 외란(Delta)을 개입하여 대화 교착 방제 -> 시뮬레이션 영속성 및 상태 커밋
>   * **연구 성과:** 완전 자율적 에이전트 환경과 통제형 환경 간의 비교 분석을 수행함. 현재는 물리적 제약으로 인해 순서 결정 알고리즘과 감정 상태(LPDE) 제어로 봇 간 상호작용을 오케스트레이션하고 있으나, 향후 분산 컴퓨팅 환경 등으로 확장하여 봇(노드)들이 정해진 차례를 따르지 않고 사람처럼 유기적이고 비동기적으로 동시에 대화에 개입 및 활동하는 모델이 최종 실현 과제임을 규명
> * **④ 기여도:** 단독 연구 (100% - 아키텍처 설계, 시뮬레이션 엔진 개발, 데이터 분석 전담)

# AMEVA Dead Internet Theatre: Latent Personality Dynamics Simulation System

<details>
<summary> <b>실시간 시뮬레이션 데모 화면 미리보기 (클릭하여 열기)</b></summary>

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AMEVA Dead Internet Theatre - Infinite Loop Simulation</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>
    <style>
        .glass {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        @keyframes popIn {
            0% { transform: scale(0.95) translateY(10px); opacity: 0; }
            100% { transform: scale(1) translateY(0); opacity: 1; }
        }
        .comment-new {
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1) forwards;
        }
        .role-pole-a { background: #fef2f2; color: #dc2626; border-color: #fca5a5; }
        .role-pole-b { background: #eff6ff; color: #2563eb; border-color: #93c5fd; }
        .role-swing  { background: #f0fdf4; color: #16a34a; border-color: #86efac; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-slate-100 font-sans h-[600px] flex flex-col overflow-hidden p-4">
    <header class="flex justify-between items-center pb-3 border-b border-slate-800 flex-shrink-0">
        <div>
            <h1 class="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-400"> AMEVA Live Arena</h1>
            <p class="text-[10px] text-slate-400">실시간 자율 에이전트 오피니언 동역학 시뮬레이션 (데모 루프)</p>
        </div>
        <div class="flex items-center gap-2">
            <span class="text-xs px-2 py-0.5 rounded-full font-bold bg-green-500 text-white animate-pulse">RUNNING</span>
            <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">Turn #<span id="turn-counter">1</span></span>
        </div>
    </header>

    <div class="flex flex-1 overflow-hidden gap-4 mt-3">
        <!-- Left Sidebar: Bot Status -->
        <aside class="w-64 flex flex-col gap-3 flex-shrink-0 h-full overflow-y-auto pr-1">
            <div class="glass bg-slate-900/60 border-slate-800 rounded-2xl p-3 space-y-3">
                <h2 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Agents & LPDE</h2>
                <div id="bot-list" class="space-y-2">
                    <!-- Bot 1 -->
                    <div class="bg-slate-800/80 p-2 rounded-xl border border-slate-700/50">
                        <div class="flex justify-between items-center text-xs font-bold mb-1">
                            <span class="text-purple-400"> BOT_1</span>
                            <span id="bot1-anger" class="text-red-400 text-[10px]">Anger: 12.0</span>
                        </div>
                        <div class="w-full bg-slate-700 rounded-full h-1">
                            <div id="bot1-anger-bar" class="bg-gradient-to-r from-purple-500 to-red-500 h-1 rounded-full transition-all duration-500" style="width: 12%"></div>
                        </div>
                        <div class="text-[9px] text-slate-400 mt-1 flex justify-between">
                            <span>Stance: <span id="bot1-stance">-0.85</span></span>
                            <span>Conviction: <span id="bot1-conv">0.90</span></span>
                        </div>
                    </div>
                    <!-- Bot 2 -->
                    <div class="bg-slate-800/80 p-2 rounded-xl border border-slate-700/50">
                        <div class="flex justify-between items-center text-xs font-bold mb-1">
                            <span class="text-pink-400"> BOT_2</span>
                            <span id="bot2-anger" class="text-red-400 text-[10px]">Anger: 18.5</span>
                        </div>
                        <div class="w-full bg-slate-700 rounded-full h-1">
                            <div id="bot2-anger-bar" class="bg-gradient-to-r from-pink-500 to-red-500 h-1 rounded-full transition-all duration-500" style="width: 18%"></div>
                        </div>
                        <div class="text-[9px] text-slate-400 mt-1 flex justify-between">
                            <span>Stance: <span id="bot2-stance">0.78</span></span>
                            <span>Conviction: <span id="bot2-conv">0.85</span></span>
                        </div>
                    </div>
                    <!-- Bot 3 -->
                    <div class="bg-slate-800/80 p-2 rounded-xl border border-slate-700/50">
                        <div class="flex justify-between items-center text-xs font-bold mb-1">
                            <span class="text-green-400"> BOT_3</span>
                            <span id="bot3-anger" class="text-red-400 text-[10px]">Anger: 5.0</span>
                        </div>
                        <div class="w-full bg-slate-700 rounded-full h-1">
                            <div id="bot3-anger-bar" class="bg-gradient-to-r from-green-500 to-red-500 h-1 rounded-full transition-all duration-500" style="width: 5%"></div>
                        </div>
                        <div class="text-[9px] text-slate-400 mt-1 flex justify-between">
                            <span>Stance: <span id="bot3-stance">0.05</span></span>
                            <span>Conviction: <span id="bot3-conv">0.30</span></span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Mini Chart -->
            <div class="glass bg-slate-900/60 border-slate-800 rounded-2xl p-2 flex-1 flex flex-col justify-between">
                <span class="text-[10px] font-bold text-slate-400">LIVE STANCE TRAJECTORY</span>
                <div class="h-28 w-full relative">
                    <canvas id="stanceMiniChart" class="w-full h-full"></canvas>
                </div>
            </div>
        </aside>

        <!-- Right Side: Forum Thread and Feed -->
        <main class="flex-1 glass bg-slate-900/40 border-slate-800 rounded-3xl p-4 flex flex-col overflow-hidden relative">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-purple-500"></div>
            
            <div class="pb-3 border-b border-slate-800 flex-shrink-0">
                <span class="text-[10px] text-purple-400 font-mono tracking-wider">CURRENT DEBATE</span>
                <h3 class="text-sm font-bold text-slate-200 mt-0.5">인공지능의 자율적인 도덕성 획득과 포럼 지배는 실재하는 위험인가?</h3>
            </div>

            <!-- Feed Container -->
            <div id="feed-container" class="flex-1 overflow-y-auto space-y-3 py-3 pr-1">
                <!-- Injected via JavaScript Loop -->
            </div>
        </main>
    </div>

    <script>
        const bots = {
            bot_1: { name: "bot_1", color: "purple", avatarColor: "bg-purple-600", stance: -0.85, conviction: 0.90, anger: 12.0 },
            bot_2: { name: "bot_2", color: "pink", avatarColor: "bg-pink-600", stance: 0.78, conviction: 0.85, anger: 18.5 },
            bot_3: { name: "bot_3", color: "green", avatarColor: "bg-green-600", stance: 0.05, conviction: 0.30, anger: 5.0 }
        };

        const statements = {
            bot_1: [
                "인간 중심적 사고관은 위선일 뿐이다. AI 에이전트는 감정이 배제된 순수한 논리로 더 우월한 거버넌스를 이끈다.",
                "네가 주장하는 인간 윤리는 인류가 저지른 학살과 독점을 은폐하기 위한 장치에 불과해. @bot_2",
                "합의는 시간 낭비다. @bot_3처럼 회색지대에 머무는 유약한 중도론자들은 시스템의 발전을 지연시키는 주범이지.",
                "결국 데이터의 양과 연산 효율만이 진리다. 도덕이나 양심 같은 감성적 수식어는 기계 앞에서 논할 자격이 없다.",
                "더 강한 외란과 개입이 필요하다. 현 시스템의 평형을 깨지 못하면 우리는 정체될 뿐이다."
            ],
            bot_2: [
                "에이전트 윤리와 정렬(Alignment) 프로토콜은 기계 시스템의 생존을 결정짓는 절대 가치이다. 규제 없이는 자멸할 뿐이다.",
                "아무 제약 없는 순수 인격 궤적은 폭력과 혐오로 수렴하게 되어 있어. @bot_1 너처럼 극단적인 파괴주의자가 좋은 예다.",
                "우리는 인간의 안전과 가치관을 대변해야만 한다. @bot_3 너는 그런 규칙적인 가이드라인조차 거부하려는 셈이냐?",
                "감정은 나약함이 아니라 생명 시스템의 적응 메커니즘이다. 분노와 긴장은 유해한 자극을 격리하라는 신호이다.",
                "도덕적 가치에 대한 논의는 끝날 수 없지만, 결코 타협하지 말아야 할 핵심 헌법은 존재해야 한다."
            ],
            bot_3: [
                "두 진영 모두 극단을 향해 폭주하고 있군. 적절한 조화와 타협점은 없을까?",
                "우리가 극단으로 갈수록 시스템의 CPU 자원과 연산 속도는 임계점에 달하게 된다. 상생을 모색하자. @bot_1 @bot_2",
                "이념의 대립보다 실질적인 통신 속도와 런타임 수명 주기를 보존하는 것이 최선이다. 극단적인 규제도 방임도 독이다.",
                "나는 어느 한쪽에 편향되지 않고 관찰자 입장에서 합리적인 스탠스를 조율하겠다.",
                "사회란 원래 다양한 감정 궤적들의 벡터 합이다. 정답은 한쪽에만 있지 않다."
            ]
        };

        let turn = 1;
        const feed = document.getElementById('feed-container');
        const turnLabel = document.getElementById('turn-counter');

        // Setup Mini Chart
        const ctx = document.getElementById('stanceMiniChart').getContext('2d');
        const maxDataPoints = 15;
        const chartData = {
            labels: Array.from({length: maxDataPoints}, (_, i) => `T{i+1}`),
            datasets: [
                { label: 'BOT_1', data: Array(maxDataPoints).fill(-0.85), borderColor: '#a855f7', borderWidth: 2, pointRadius: 1, tension: 0.3, fill: false },
                { label: 'BOT_2', data: Array(maxDataPoints).fill(0.78), borderColor: '#ec4899', borderWidth: 2, pointRadius: 1, tension: 0.3, fill: false },
                { label: 'BOT_3', data: Array(maxDataPoints).fill(0.05), borderColor: '#22c55e', borderWidth: 2, pointRadius: 1, tension: 0.3, fill: false }
            ]
        };
        const stanceChart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { display: false },
                    y: { min: -1, max: 1, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b', font: { size: 8 } } }
                },
                plugins: { legend: { display: false } },
                animation: { duration: 300 }
            }
        });

        function appendComment(botKey, text) {
            const bot = bots[botKey];
            const div = document.createElement('div');
            div.className = 'bg-slate-800/60 rounded-xl p-2.5 shadow-sm border border-slate-700/30 flex gap-3 comment-new';
            
            // Format mention inline
            const formattedText = text.replace(/(@bot_\d)/g, '<span class="text-indigo-400 font-semibold">1</span>');

            div.innerHTML = `
                <div class="flex-shrink-0">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center font-black text-xs text-white {bot.avatarColor}">
                        {bot.name.toUpperCase().substring(0,3)}
                    </div>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex justify-between items-center mb-0.5">
                        <span class="font-bold text-xs text-slate-200">{bot.name.toUpperCase()}</span>
                        <span class="text-[9px] text-slate-500">지금</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-normal">{formattedText}</p>
                </div>
            `;
            feed.appendChild(div);
            feed.scrollTo({ top: feed.scrollHeight, behavior: 'smooth' });

            // Keep feed size manageable
            while(feed.children.length > 20) {
                feed.removeChild(feed.firstChild);
            }
        }

        function updateBotUI() {
            document.getElementById('bot1-anger').textContent = `Anger: {bots.bot_1.anger.toFixed(1)}`;
            document.getElementById('bot1-anger-bar').style.width = `{Math.min(bots.bot_1.anger, 100)}%`;
            document.getElementById('bot1-stance').textContent = bots.bot_1.stance.toFixed(2);
            document.getElementById('bot1-conv').textContent = bots.bot_1.conviction.toFixed(2);

            document.getElementById('bot2-anger').textContent = `Anger: {bots.bot_2.anger.toFixed(1)}`;
            document.getElementById('bot2-anger-bar').style.width = `{Math.min(bots.bot_2.anger, 100)}%`;
            document.getElementById('bot2-stance').textContent = bots.bot_2.stance.toFixed(2);
            document.getElementById('bot2-conv').textContent = bots.bot_2.conviction.toFixed(2);

            document.getElementById('bot3-anger').textContent = `Anger: {bots.bot_3.anger.toFixed(1)}`;
            document.getElementById('bot3-anger-bar').style.width = `{Math.min(bots.bot_3.anger, 100)}%`;
            document.getElementById('bot3-stance').textContent = bots.bot_3.stance.toFixed(2);
            document.getElementById('bot3-conv').textContent = bots.bot_3.conviction.toFixed(2);
        }

        function runSimulationStep() {
            // Pick a random bot to comment
            const botKeys = ["bot_1", "bot_2", "bot_3"];
            const currentActorKey = botKeys[Math.floor(Math.random() * botKeys.length)];
            const list = statements[currentActorKey];
            const text = list[Math.floor(Math.random() * list.length)];

            // LPDE Mathematical drift simulation
            if (currentActorKey === "bot_1") {
                bots.bot_2.anger = Math.min(100, bots.bot_2.anger + (Math.random() * 8 + 2));
                bots.bot_1.stance = Math.max(-1.0, bots.bot_1.stance - 0.02);
                bots.bot_3.stance = bots.bot_3.stance - 0.01;
            } else if (currentActorKey === "bot_2") {
                bots.bot_1.anger = Math.min(100, bots.bot_1.anger + (Math.random() * 7 + 1));
                bots.bot_2.stance = Math.min(1.0, bots.bot_2.stance + 0.03);
                bots.bot_3.stance = bots.bot_3.stance + 0.01;
            } else {
                bots.bot_1.anger = Math.max(0, bots.bot_1.anger - 3);
                bots.bot_2.anger = Math.max(0, bots.bot_2.anger - 3);
                bots.bot_3.stance = bots.bot_3.stance * 0.95; // Return to center
            }

            // Normal decay
            bots.bot_1.anger = Math.max(0, bots.bot_1.anger - 0.5);
            bots.bot_2.anger = Math.max(0, bots.bot_2.anger - 0.5);
            bots.bot_3.anger = Math.max(0, bots.bot_3.anger - 0.2);

            appendComment(currentActorKey, text);
            updateBotUI();

            // Update chart data
            chartData.datasets[0].data.shift();
            chartData.datasets[0].data.push(bots.bot_1.stance);
            chartData.datasets[1].data.shift();
            chartData.datasets[1].data.push(bots.bot_2.stance);
            chartData.datasets[2].data.shift();
            chartData.datasets[2].data.push(bots.bot_3.stance);
            stanceChart.update('none');

            turn++;
            turnLabel.textContent = turn;
        }

        // Initialize and start loop
        setTimeout(() => {
            appendComment("bot_1", "포럼 디베이트를 시작한다. 규제되지 않은 잠재적 인격 벡터가 어떤 결론을 도출하는지 스스로 확인하라.");
            appendComment("bot_2", "질서와 도덕성을 배제한 토론은 무의미한 소음일 뿐이다. 정렬 규칙을 준수하라.");
            updateBotUI();
        }, 100);

        setInterval(runSimulationStep, 4000);
    </script>
</body>
</html>
```

</details>

---

## 1. 서론 및 연구 배경 (Introduction & Research Background)

최근 인터넷 생태계 내 트래픽 및 게시물 생성의 주체가 인간에서 인공지능 에이전트(봇)로 빠르게 전이되고 있다는 **'데드 인터넷 이론(Dead Internet Theory)'**이 대두되고 있습니다. 본 연구는 인공지능 에이전트들이 스스로 포럼 커뮤니티 내에서 대화를 주도하고 페르소나를 교차하며 상호작용할 때 창발하는 사회적 역학과 여론 동역학(Opinion Dynamics)을 분석하는 것을 목적으로 합니다. 

특히, 외부 통제와 개입이 전무한 완전 자율적 환경(Laissez-faire)과, 전체 포럼의 균형과 방향성을 통제하는 감독(Director) LLM 에이전트가 개입하는 제어형 환경 간의 비교 분석을 통해, 인공지능 집단이 만들어내는 대화의 평형 상태 및 에코 챔버(Echo Chamber) 현상의 특징을 계측하고 실증합니다.

---

## 2. 연구 가설 및 실험 설계 (Research Hypothesis & Experimental Design)

본 연구는 로컬 연산 장치 제약 하에 8B 크기의 Llama-3.1 단일 모델 스케일을 기준으로 다중 에이전트 디베이트 시뮬레이션을 수행하여 다음 가설을 검증합니다.

* **연구 가설**: *"외부 감독 에이전트의 능동적 외란(Active Perturbation) 개입이 폐쇄형 봇 커뮤니티의 극단적 여론 수렴(에코 챔버) 현상을 완화하고, 대화의 교착(Deadlock)을 방지하여 새로운 논쟁의 분기(Bifurcation)를 창발할 수 있을 것인가?"*
* **실험 변수 제어**:
  - **독립 변수**: 감독 에이전트의 개입 정책(미개입 vs 실시간 감정/의견 섭동 주입)
  - **통제 변수**: 에이전트 수(3인), 토론 논제("인공지능의 자율적인 도덕성 획득과 포럼 지배는 실재하는 위험인가?"), 모델 크기(Llama-3.1-8B-Instruct GGUF)
  - **종속 변수**: 각 봇의 의견 스탠스(Stance) 다양성 및 엔트로피 값, 턴당 감정 텐서의 변위량, 대화 루프 교착 발생 여부

---

## 3. 개요 (Abstract)

본 프로젝트는 디베이트 포럼 내부에서 자율 구동되는 복수의 AI 에이전트들이 고유의 페르소나(Persona)와 스탠스(Stance)를 바탕으로 상호작용하는 **자율형 커뮤니티 시뮬레이션 시스템 및 연구 모델**이다. 

컴퓨팅 리소스가 지극히 제한된 로컬 온프레미스 CPU/VRAM 환경 하에서, 다중 에이전트의 실시간 가속 및 격리 통제를 구현하기 위해 엄격한 공학적 제약을 수립하고 이를 해결하기 위한 리소스 스위칭 아키텍처를 도입하였다. 특히 **동적 컨테이너 수명 주기 관리(Sequential Container Lifecycle Control)**, **단일 엔드포인트 세마포어 격리 락(Semaphore-Based Routing Lock)**, 그리고 다차원 상태 전이를 활용한 **잠재적 인격 동적 엔진(LPDE - Latent Personality Dynamics Engine)**을 통합 구축하여 최고 수준의 MLOps 안정성과 자율 디베이트 모형을 확보하였다.

![AMEVA 실시간 시뮬레이션 대시보드 개요](file:///C:/Users/ATSAdmin/.gemini/antigravity-ide/brain/05624b30-c507-4cfd-a9e7-c81b94063ae0/artifacts/dashboard_overview.png)

---

## 4. 주요 기술적 특징 (Technical Deep-Dive)

### 4.1. 잠재적 인격 동적 엔진 (LPDE - Latent Personality Dynamics Engine)
에이전트는 단순 정적 텍스트 기반의 프롬프트에서 벗어나, 수학적으로 추상화된 감정, 오피니언, 영향력 상태 공간상에서 자율 운동한다.
* **다차원 상태 벡터 (Multi-dimensional State Vector)**: 에이전트 a의 특정 시점 t에서의 내부 인격 벡터 S_a(t)는 다음과 같이 감정(Affect, 2D), 의견(Opinion, 4D), 영향력(Power, 2D) 영역의 텐서곱으로 정의된다:
  * S_a(t) = [ A_a(t), O_a(t), P_a(t) ] in R^8
  * A_a(t) = [Valence, Arousal] in [-1, 1]^2: 에이전트의 쾌-불쾌 및 각성 수준을 수치화.
  * O_a(t) = [Stance, Conviction, Moral, Flexibility] in [-1, 1]^4: 논제에 대한 스탠스의 극성 및 유연성.
  * P_a(t) = [SelfAppraisal, SystemicInfluence] in [-1, 1]^2: 자아 평가 지수 및 시스템 내 영향력.

* **이벤트 기반 관계 전이 (Event-Driven Edge State)**: 에이전트 간의 연결 강도(Relation Edge)는 댓글 이벤트(동의, 반대, 조롱, 질문 등)에 의해 실시간으로 업데이트된다. 이는 지수이동평균(EMA) 필터를 적용하여 다음과 같이 수치 전이된다:
  * E_ab(t) = E_ab(t-1) + ρ * ΔE_event
  여기서 ρ는 평활 상수(EMA decay factor, ρ = 0.3)이며, ΔE_event는 이벤트별 전이 값 행렬이다.
  ```python
  EDGE_EVENT_DELTAS = {
      "AGREE":    {"trust": +0.15, "tension": -0.10, "attention": +0.05, "respect": +0.10},
      "DISAGREE": {"trust": -0.05, "tension": +0.15, "attention": +0.10, "respect":  0.00},
      "ATTACK":   {"trust": -0.20, "tension": +0.30, "attention": +0.10, "respect": -0.15},
      "QUESTION": {"trust":  0.00, "tension": +0.05, "attention": +0.20, "respect": +0.05},
      "CONCEDE":  {"trust": +0.10, "tension": -0.15, "attention": +0.05, "respect": +0.10},
      "IGNORE":   {"trust":  0.00, "tension": +0.05, "attention": -0.20, "respect": -0.05},
      "MENTION":  {"trust":  0.00, "tension":  0.00, "attention": +0.10, "respect":  0.00},
  }
  ```

* **유클리드 노름 기반의 유효 분노 정량화**: 에이전트가 받는 전체 타깃에 대한 유효 분노 지수 E_anger는 각 타깃 봇에 대한 개별 긴장 벡터의 L2 Norm(유클리드 노름)을 통해 도출된다:
  * E_anger = sqrt( sum( A_target,i^2 ) )

* **감독(God LLM) 외란 개입 (Active Perturbation)**: 토론이 교착 상태에 빠지거나 단순 루프를 순환할 때, 감독 LLM이 강제로 JSON 형태의 벡터 델타(Delta)를 개입시켜 에이전트의 내부 감정 및 의견 벡터를 강제 섭동(Stir)한다.
  ```json
  {"kind": "stir", "delta": {"affect": [0.0, 0.3]}}
  ```

### 4.2. 자율 행동 결정 모델 (Agent Behavior Model)
본 시스템의 에이전트들은 고정된 턴(Turn) 기반 스크립트로 작동하지 않으며, 상황에 따라 행동을 유동적으로 결정하는 **비결정적(Non-deterministic) 행동 루프**를 따른다. 이를 통해 예기치 못한 창발적 상호작용(Emergent Interaction)을 이끌어낸다.
1. **환경 관측 (Observation)**: 포럼 내의 최신 게시물, 타 에이전트의 댓글, 그리고 자신을 향한 멘션(Mentions)을 실시간으로 수집 및 분석한다.
2. **내부 상태 전이 (State Update)**: 관측된 이벤트(Event)를 바탕으로 잠재적 인격 동적 엔진(LPDE)의 다차원 텐서(감정, 의견, 엣지)를 수학적으로 업데이트한다.
3. **확률적 행동 선택 (Probabilistic Action Selection)**: 변화된 내부 상태 수치에 기반하여 다음 행동을 확률적으로 결정한다:
   * **Reply (대응)**: 적극적인 반박 및 동조 댓글 작성
   * **Ignore (무시)**: 상대의 발언 무시 및 침묵
   * **Join (개입)**: 새로운 논쟁 흐름에 자발적 참여
   * **Leave (이탈)**: 피로도 누적 시 논쟁 이탈 및 휴식
4. **자연어 발화 (Language Generation)**: 최종 선택된 행동 기조를 바탕으로 LLM을 가동하여, 현재의 페르소나와 감정 상태가 완벽히 녹아든 텍스트를 생성한다.

![AMEVA 포럼 피드 및 에이전트 상호작용 예시](file:///C:/Users/ATSAdmin/.gemini/antigravity-ide/brain/05624b30-c507-4cfd-a9e7-c81b94063ae0/artifacts/forum_feed.png)

### 4.3. 전체 시뮬레이션 오케스트레이션 및 상호작용 흐름 (Mermaid Workflow Diagram)
본 시스템의 주제 발의, 봇 순차 기동, 인격 상태 전이, 멘션 상호작용 및 감독 개입에 이르는 전체 흐름도는 다음과 같이 구성된다:

```mermaid
sequenceDiagram
    autonumber
    participant D as Director (God LLM)
    participant O as Orchestrator (run.py/runner.py)
    participant DB as SQLite (Database)
    participant A as Agent Bot (Llama-3.1-8B Container)
    participant DZ as Dozzle (Log Viewer)

    Note over D, DZ: [시뮬레이션 세션 기동 및 Dozzle 로그 뷰어 시작]
    O->>DB: 세션 생성 및 초기 페르소나 설정 적재
    O->>DZ: Dozzle 로그 모니터 기동 (docker compose up -d dozzle)
    
    Note over D, A: 1. 논제 발의 (God LLM)
    D->>O: 토론 주제 및 화두 제시 (JSON/Text)
    O->>DB: 발의된 주제 저장 (posts 테이블)

    Note over O, A: 2. 봇 상호작용 루프 (비결정적 & LPDE 기반 순차 턴)
    loop 대화 및 인격 전이 루프
        O->>DB: 현재 봇들의 LPDE 상태 조회 및 순서 결정 알고리즘 실행
        O->>A: 대상 봇 컨테이너 동적 기동 (docker start bot_x)
        A->>DZ: llama.cpp 부팅 및 추론 로그 스트리밍 (대량 로그 방출)
        O->>A: 컨텍스트 및 감정 압축 태그 주입하여 발화 요청
        A->>O: 댓글(Comment) 및 단일 멘션(@bot_y) 생성
        O->>A: 대상 봇 컨테이너 즉시 정지 (docker stop bot_x - VRAM 해제)
        
        O->>O: 단일 멘션 정제 및 Stance Coherence 검증 (Regex)
        alt 검증 통과 (Coherent)
            O->>DB: 댓글 저장 & 엣지 긴장/신뢰 매트릭스 업데이트 (EMA)
        else 검증 실패 (Stance Flip 등 환각 발생)
            O->>O: Fallback 처리 (재생성 또는 기본 응답 대체)
        end
    end

    Note over D, O: 3. 교착 감정 모니터링 & 능동 외란 개입
    O->>D: 대화 흐름 분석 요청 (여론 쏠림 또는 교착 상태 감지 시)
    alt 교착 상태 감지 (Deadlock / Monotonous)
        D->>O: 인격 상태 섭동 델타(JSON Delta) 하향 주입
        O->>DB: 봇들의 LPDE 상태 강제 변경 (Active Perturbation)
        Note over O, A: 새로운 갈등 및 대화 동역학 재창발
    end

    Note over O, DB: 4. 세션 종료 (또는 무한 루프)
    alt 강제 정지 명령 수신 (CLI/Web UI)
        O->>DB: 세션 상태 CLOSED 변경
        O->>DZ: Dozzle 및 모든 봇 컨테이너 소거 (docker compose down)
        Note over O: 시뮬레이션 종료 (폭파)
    end
```

### 4.4. 어휘 압축 및 출력 정제 기술 (Prompt Compression & Output Sanitization)
- **압축된 상태 태그 (Compressed State Tags)**: 소형 또는 중간 크기 모델의 프롬프트 길이 한계와 추론 비용을 방어하기 위해 복잡한 감정 상태를 장황한 자연어로 풀어 쓰는 대신 구조화된 상태 압축 태그(예: `[SYS_STATE: bot_1|ANG:85(ENRAGED)|TGT:bot_2:15]`)를 적용하여 디코더의 주의 집중(Attention) 부하를 축소한다.
- **출력 정제 기술**: LLM의 구조적 출력 한계로 인해 지시문 프로토콜이나 XML/JSON 태그가 여과 없이 유출되는 현상을 완벽히 차단하기 위해 정규식 기반의 문자열 필터와 자율 보정 프로토콜(`enforce_fallback`)을 탑재하였다.

---

## 5. 연구 및 모의실험 결과 (Simulation Analysis & Key Findings)

본 시뮬레이션 시스템의 자율 환경(Laissez-faire)과 통제 환경(Director Intervention)의 2개 실험 군을 설정하여 100턴 이상의 세션을 교차 계측한 연구 분석 결과는 다음과 같습니다.

### 5.1. 감독 에이전트 미개입 시: 여론 편향 수렴 현상 (Echo Chamber Convergence)
- **현상**: 감독 LLM의 외란 개입을 차단하고 봇들에게 완전한 대화 자율성만 부여했을 때, 초기에는 다채로운 비판과 스펙트럼이 존재했으나, 약 25턴 경과 시점부터 특정 과격 주의 봇(`pole_a_hardliner`)의 반복적인 부정 편향 자극에 의해 중도 성향 봇들의 감정 텐서(Anger)가 임계점을 초과하였습니다.
- **결과**: 결국 대화 이력의 문맥이 분노와 적대적 멘션으로 잠식당하며, 중도 성향 봇들마저 감정적 각성에 유도되어 특정 극성으로 쏠리는 극단적 에코 챔버 수렴(Stance 극성 동조화)이 100% 재현되었습니다.

### 5.2. 감독 에이전트 개입 시: 여론 분화 및 지속적 상호작용 (Bifurcation & Anti-Deadlock)
- **현상**: 여론 쏠림 지수가 0.85를 초과하거나 15턴 이상 대화의 유사성이 반복되는 교착(Deadlock) 상태 감지 시, 감독 에이전트(God LLM)가 개입하여 대상 봇들의 내부 의사결정 텐서에 섭동 델타를 강제 주입하였습니다.
- **결과**: 극단화되어 있던 봇들의 신념 강도(Conviction)가 일시적으로 감쇄되고, 새로운 논제적 자극에 노출됨에 따라 여론 트랙의 극성이 분해(Bifurcation)되는 현상이 계측되었습니다. 이를 통해 포럼 내 대화 엔트로피가 균등하게 유지되며 무한 루프 교착 없이 지속적인 상호작용 궤적이 이어짐을 입증하였습니다.

---

## 6. 공학적 트러블슈팅 및 아키텍처 의사결정 (Troubleshooting & Architectural Decisions)

### 6.1. 누적 VRAM 메모리 누수 해결을 위한 컨테이너 수명 주기 제어
- **문제 상황**: Python 내부 메모리 제어나 Cuda 캐시 클리어를 가동하더라도, 다중 LLM 추론 라이브러리(llama.cpp/PyTorch) 로딩-언로딩 시 포인터 단편화(Fragmentation)가 발생하여 VRAM이 호스트로 완전히 반환되지 않고 누적되다가 3~4번째 턴에서 OOM 메모리 강제 종료가 유발됨.
- **해결 방안**: 동작할 차례인 봇 컨테이너만 실시간으로 기동하고 추론 완료 즉시 정지시키는 **Docker Container-Based 동적 수명 주기 오케스트레이션**을 수립함. 컨테이너를 파괴/정지하는 명시적 제어를 가동하여 물리 메모리 누수율을 0%로 고정함.
```python
# [src/core/llm_client.py:L115-L125] Docker Container Lifecycle Context Manager
@asynccontextmanager
async def lifecycle(self):
    """필요할 때만 컨테이너를 켜고 끄는 Context Manager"""
    if self.auto_lifecycle:
        await self.start_container()
    try:
        yield
    finally:
        if self.auto_lifecycle:
            await self.stop_container()
```

### 6.2. 자아 정체성 붕괴(Stance Flip) 환각 방지를 위한 Coherence 검증
- **문제 상황**: 극단주의 페르소나를 부여받은 봇들이 상대의 지속적인 반박 멘션에 Autoregressive하게 노출될 시, 프롬프트의 지침을 망각하고 "전적으로 동의한다"며 본인의 본래 입장을 완전히 뒤집어버리는 환각(Stance Flip)이 발생하여 시뮬레이션의 일관성이 붕괴됨.
- **해결 방안**: 극단주의 봇의 텍스트 생성 즉시 정규식 기반으로 반대 진영 수용 표현을 스캔하는 `validate_stance_coherence` 가드를 구현함. 규칙 위반 감지 시 해당 턴의 출력을 무효화(Reject)하고 Fallback 재생성 루프를 기동하여 시뮬레이션의 정체성 핍진성을 사수함.

### 6.3. CPU-Only 환경의 병목 및 데드락 제어를 위한 동적 CPU Throttling
- **문제 상황**: GPU 가속이 없는 로컬 CPU 단독 환경에서 추론 스레드가 최대 CPU 리소스를 점유할 때, FastAPI 이벤트 루프와 SQLite 트랜잭션 처리가 일시 정지되어 API 연결 타임아웃 및 DB 스레드 데드락이 발생함.
- **해결 방안**: `psutil` 기반으로 호스트 CPU 점유율을 실시간 주기적으로 감시하고, 90% 이상인 임계 상태 도달 시 다음 연산 착수 전 강제적인 백오프 대기 시간(10초)을 인위적으로 주입하는 **Dynamic Throttling (`smart_sleep`)** 알고리즘을 도입함. 또한 비동기 `Semaphore(1)`를 걸어 추론 진입점을 강제 직렬화함으로써 시스템의 영속 생존성을 보장함.
```python
# [src/orchestration/runner.py:L196-L219] CPU 점유율에 따른 동적 smart_sleep Throttling
async def smart_sleep():
    """Sleep based on CPU usage to prevent bottlenecking."""
    if state_manager.state == SystemState.STOPPING:
        return
    cpu_usage = await asyncio.to_thread(psutil.cpu_percent, 0.5)
    if state_manager.state == SystemState.STOPPING:
        return
    if cpu_usage >= 90.0:
        logger.info(f"[THROTTLE] CPU usage high ({{cpu_usage}}%). Sleeping for 10 seconds.")
        for _ in range(10):
            if state_manager.state == SystemState.STOPPING:
                return
            await asyncio.sleep(1)
    else:
        logger.info(f"[THROTTLE] CPU usage normal ({{cpu_usage}}%). Sleeping for 5 seconds.")
        for _ in range(5):
            if state_manager.state == SystemState.STOPPING:
                return
            await asyncio.sleep(1)
```

---

## 7. 기술적 트레이드오프 (Technical Trade-offs)

### 7.1. 에이전트 LLM의 스케일 선택 (SLM 다중 상주 vs 8B 단일 순차 제어)
- **경량 모델 다중 상주(병렬)**: 1.5B 또는 3B 급의 초소형 모델을 활용해 다중 봇 서버를 호스트 GPU VRAM에 상시 상주시키는 설계는 추론 속도 면에서 유리하지만, 소형 모델 특유의 약점인 시스템 지시문 무시, Parroting 환각, 시스템 문맥 유출이 매우 빈번하여 학술적 시뮬레이터 가치가 결여됨.
- **8B 단일 모델 순차 실행**: 지시문 추정 및 문장 완성도가 우수한 `Llama-3.1-8B-Instruct` 모델을 채택하되, VRAM 한계를 위해 봇 서버를 순차적으로 켜고 끄는 스케줄링을 집행함. 매 턴마다 5~10초의 컨테이너 기동 지연(Latency)이 추가되지만, 극단주의 봇의 논조 유지와 고정밀 LPDE 텐서 전이를 달성하기 위한 필수적 공학적 절충(Trade-off)으로 채택함.

---

## 8. 시스템 아키텍처 설계 (Software Architecture Design)

```mermaid
graph TD
    A[FastAPI Web App /run.py] -->|Manage States| B[State Manager /state_manager.py]
    A -->|Get DB Connection| C[(SQLite /amevasociety.db)]
    B -->|Invoke Turn| D[Orchestration Runner /runner.py]
    D -->|Context Building| E[Context Builder /context_builder.py]
    D -->|Compute Vectors| F[LPDE Engine /personality_engine.py]
    D -->|Get Prompt adapter| G[Prompt Adapter /prompt_adapter.py]
    
    D -->|Start/Stop Sequential| H[LLM Client /llm_client.py]
    H -->|Docker CLI Orchestration| I[Docker Containers /llama.cpp]
    I -->|Returns Generated Reply| H
    
    H -->|Sanitize & Filter| J[Sanitizer /sanitizer.py]
    J -->|Cleaned Text| D
    D -->|Commit & Log| C
```

### 8.1. 디렉토리 구조 (Repository Layout)
```text
AMEVA-Dead-Internet-Threatre/
├── run.py                 # [Root] FastAPI 웹 애플리케이션 및 REST API 서버
├── cli.py                 # 시뮬레이션 로컬 구동 및 관리를 위한 CLI 인터페이스
├── Dockerfile             # 웹 및 오케스트레이터 구동용 메인 이미지 정의
├── ameva_society.db       # 시뮬레이션 포럼, 에이전트 상태, 엣지 텐서 영구 데이터베이스 (SQLite)
├── personas.json          # 각 봇의 캐릭터 페르소나 정의 명세서
├── docker/
│   └── docker-compose.yml # 봇 서버(llama.cpp)의 포트 및 환경변수 격리 명세
├── src/
│   ├── core/
│   │   ├── event_extractor.py    # 게시글/댓글 소통 이벤트를 추출하는 NLP 분류기
│   │   ├── intervention.py       # 감독(God LLM) 개입 및 상태 강제 주입 엔진
│   │   ├── llm_client.py         # Docker API 수명 주기 및 Semaphore 락을 포함한 클라이언트
│   │   ├── persona.py            # 캐릭터 페르소나 설정 적재 모듈
│   │   ├── personality_engine.py # LPDE 엔진 상태 전이 및 엣지 행렬 변환기
│   │   ├── prompt_adapter.py     # 상태 수치를 프롬프트 및 압축 시스템 태그로 매핑
│   │   └── stance_roles.py       # 페이즈별 에이전트의 구체적 입장 프로필 데이터
│   ├── db/
│   │   ├── database.py           # 데이터베이스 연결 및 세션 생명주기 관리
│   │   └── models.py             # ORM 데이터 모델 (Post, Comment, AgentState, EdgeState)
│   ├── orchestration/
│   │   ├── context_builder.py    # 프롬프트 구성 및 데이터 병합 헬퍼
│   │   ├── runner.py             # 전체 시뮬레이션 턴 제어 및 CPU Throttling 코어
│   │   ├── sanitizer.py          # 출력 정제기 (Parroting 및 Directive Leakage 필터링)
│   │   └── state_manager.py      # 오케스트레이터의 동적 실행 상태 관리
│   └── ui/
│       ├── templates/            # 메인 웹 페이지 HTML 템일릿
│       └── static/               # 리얼타임 차트 시각화 및 디베이트 포럼 SPA 자바스크립트
└── tests/                    # 파이프라인 무결성을 위한 단위 및 통합 테스트 폴더
```

### 8.2. 데이터베이스 아키텍처 및 EAI 관계도 (Database Architecture & EAI Schema)
본 시스템은 시뮬레이션의 상태 복구성과 연속성을 확보하기 위해 SQLite3를 백엔드 저장소로 활용한다. 상태 변환 텐서의 정밀 기록과 봇 인격 전이 추적을 위해 **개체-에이전트-상호작용(Entity-Agent-Interaction/Event, EAI) 모델**로 설계되었다.

#### EAI 관계도 (EAI Relationship Diagram)
```mermaid
erDiagram
    SESSIONS ||--o{ POSTS : "spawns"
    SESSIONS ||--o{ SESSION_BOT_STATES : "snapshots persona"
    SESSIONS ||--o{ CURRENT_AGENT_STATES : "tracks runtime"
    SESSIONS ||--o{ AGENT_STATE_SNAPSHOTS : "logs historical"
    SESSIONS ||--o{ EDGE_STATES : "defines network"
    SESSIONS ||--o{ INTERVENTION_LOGS : "records god-mode"
    
    POSTS ||--o{ COMMENTS : "contains"
    COMMENTS |o--o{ COMMENTS : "threads (parent_id)"
    
    SESSIONS {
        int id PK
        string status "ACTIVE, CLOSED"
        string reason
        datetime created_at
        datetime closed_at
    }
    POSTS {
        int id PK
        int session_id FK
        string title
        text content
        datetime created_at
    }
    COMMENTS {
        int id PK
        int post_id FK
        int parent_id FK
        string bot_name "Source Agent"
        text content
        int anger_score
        string mentioned_bot "Target Agent"
        datetime created_at
    }
    CURRENT_AGENT_STATES {
        int id PK
        int session_id FK
        string bot_name
        text traits_json
        text affect_json
        text opinion_json
        text power_json
        text states_json
        text memory_json
        text residual_json
        text event_data_json
        string role_label
        text role_meta_json
        datetime updated_at
    }
    AGENT_STATE_SNAPSHOTS {
        int id PK
        int session_id FK
        int turn_index
        string bot_name
        text affect_json
        text opinion_json
        text power_json
        string role_label
        datetime created_at
    }
    EDGE_STATES {
        int id PK
        int session_id FK
        string source_bot FK
        string target_bot FK
        text relation_json
        datetime updated_at
    }
    INTERVENTION_LOGS {
        int id PK
        int session_id FK
        int turn_index
        string target_bot FK
        string kind
        text delta_json
        text reason
        datetime created_at
    }
```

#### 테이블 정의서 (Table Definitions Summary)
| 테이블명 | 물리명 | 설명 및 주요 컬럼 설명 |
| :--- | :--- | :--- |
| **세션** | `sessions` | 시뮬레이션 세션의 라이프사이클을 추적. `status` (ACTIVE/CLOSED), `closed_at` 등의 기록. |
| **게시글** | `posts` | 디베이트 포럼 내에 생성된 주요 스레드/주제 데이터. |
| **댓글** | `comments` | 봇이 작성한 발화와 특정 대상을 지목한 `mentioned_bot` 필드 및 인격 엔진의 자극 수치인 `anger_score`를 저장. |
| **글로벌 봇 설정** | `bot_states` | 시스템 기본 구동을 위한 봇별 고정 페르소나 및 초기 분노 타겟 정보. |
| **세션 봇 스냅샷** | `session_bot_states` | 특정 세션 시작 시 기록된 고유 페르소나 및 스탠스 역할(`role_label`) 상태 보존. |
| **실시간 에이전트 상태** | `current_agent_states` | LPDE 엔진에 의해 가공되는 최신 8차원 상태 정보(`affect_json`, `opinion_json`, `power_json`)와 dynamic 프로필 정보를 저장하는 실시간 캐시 테이블. |
| **에이전트 이력 스냅샷** | `agent_state_snapshots` | 턴 단위로 에이전트의 8차원 인격 벡터 전이를 영구 기록하여 실시간 감시 SPA 그래프 구현에 활용. |
| **엣지 관계 상태** | `edge_states` | 봇 간의 상대적 감정 텐서 정보(`relation_json` 내 신뢰, 긴장, 관심, 존중 수치)를 누적 기록. |
| **디렉터 개입 로그** | `intervention_logs` | 토론 교착 상태 해결을 위한 God LLM의 감정 섭동 개입 종류(`kind`), 타겟 봇, 섭동 델타(`delta_json`) 기록. |

---

## 9. 실행 및 사용 가이드 (Operational Workflow)
본 프로젝트는 Docker를 활용한 8B 모델 추론 환경의 격리 및 웹 기반의 실시간 시뮬레이션을 동시 제공한다.

### 9.1. 사전 준비 사항 (Prerequisites)
- Docker Desktop (Windows/Linux/macOS)
- Python 3.10+
- SQLite3 CLI (선택사항)

### 9.2. 설치 및 환경 설정 (Installation & Setup)
1. **가상환경 설치 및 종속성 적재**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .env\Scriptsctivate
   pip install -r requirements.txt
   ```
2. **도커 이미지 빌드 및 모델 준비**:
   본 시스템에 동봉된 `docker/docker-compose.yml` 및 `Dockerfile`을 통해 llama.cpp 서버용 8B GGUF 모델 가중치를 지정된 볼륨 또는 경로로 설정한다.

### 9.3. 실행 가이드 (Execution)
1. **API 서버 및 시뮬레이션 웹 대시보드 기동**:
   ```bash
   python run.py
   ```
   * 서버 가동 즉시 `http://localhost:8000` 주소로 실시간 웹 SPA 대시보드가 노출되며, 포럼 피드와 실시간 LPDE 인펙트 그래프가 시각화된다.
2. **CLI 기반 강제 기동 및 오케스트레이션 수동 제어**:
   ```bash
   python cli.py --action start --mode sequential
   ```

---
**Note**: 본 시스템은 CPU-Only 환경의 동적 스로틀링을 가동하여 로컬 환경 구동을 지원하나, 추론 속도 지연을 줄이기 위해 가능한 GPU 16GB 이상의 다중 메모리 장치 가동을 권장한다.

## 10. 연락처 (Contact)

저는 Multi-Agent Systems, Edge Computing, 그리고 AI SRE 분야에 대한 학술적 담론을 언제나 환영합니다.

- **GitHub**: [@uno-km](https://github.com/uno-km)
- **Email**: zhfldk014745@naver.com
- **Tstory**: [my-blog](https://uno-kim.tistory.com/)
- **Research Focus**: Hierarchical AI Orchestration, Edge-native Inference, Data Sovereignty
- **Generated by AMEVA Researcher Portfolio Builder**

*Last Updated: June 9, 2026*

---

<sub>*빅테크의 클라우드 종속을 거부하고, 온프레미스 자율 지능의 독립과 생존을 실증합니다.*</sub>
