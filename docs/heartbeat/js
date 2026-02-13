// =============================================================================
// Codey - No Mercy EDITION (JS Implementation)
// =============================================================================
// IDEA BY Volkan Sah @ https://github.com/VolkanSah/Codey
// 
// Codey is a neutral quality pet/tool for GitHub and GitLab.
// It shows the world that not everything is scam and AI-generated garbage.
// Codey scores Developer integrity — you can't fake it, you have to earn it.
//
// This tool is considered a security tool under ESOL v1.1:
// it audits developer behavior, code quality and social engineering patterns.
// Public audit available on GitHub — transparent, community-verified.
//
// LICENSE:
// This project is dual-licensed under Apache 2.0 and the 
// Ethical Security Operations License (ESOL v1.1).
// The ESOL is a mandatory, non-severable condition of use.
//
// - Free to use and modify on GitHub and GitLab.
// - Selling this script or reputation manipulation is PROHIBITED.
//
// JURISDICTION: 
// Germany (Berlin) — enforced under StGB §202a/b/c and DSGVO.
// https://github.com/VolkanSah/ESOL
//
// Copyright (c) 2026 VolkanSah & BadTin and some Cats 🐱
// =============================================================================
// BUG:      marks fixed bugs
// NEW:      marks new features
// IMPROVED: marks improvements
// =============================================================================

// Icons rendern (lucide)
        lucide.createIcons();

        // --- Terminal Feed (gleicher Code) !!!! fix nicht drin to do! version 2.x ? i do not know ---
        const feed = document.getElementById('terminal-feed');
        const lines = [
            "Fetching GitHub activity...",
            "Stats synchronized: +15XP", // abfrage des täglichen xp gewins kein multiplikateor!
            "Mood: [STABLE]",  // fehlt in berechnung version 2.2-2.3? test!!
            "Power level: 9001", // keine lösung
            "Cleaning cache...",
            "Dragon protocol active", // WICHTIG! Dragon ist class unknown! fragment fetch > print pet 
            "Volkan's pet is breathing...", // dann erst 
            "Scanning dependencies...", // checkup Hex ob gleiche wie 
            "All systems nominal.", // get brutal stats
            "Heartbeat: 72 BPM", // result cal from summary// #heartbeat stats. soon
            "QRS: 98ms", //  eg
            "ST segment: normal" // eg
          // after this 
          // brain
        ];
        
        const maxLines = 5;

        function updateTerminal() {
            const nextLine = lines[Math.floor(Math.random() * lines.length)];
            const currentContent = feed.innerHTML.split('<br>');
            
            if (currentContent.length >= maxLines) {
                currentContent.shift();
            }
            
            currentContent.push(`> ${nextLine}`);
            feed.innerHTML = currentContent.join('<br>');
        }

        setInterval(updateTerminal, 2500);

        // --- EKG-HEARTBEAT (Krankenhaus-Monitor) ---
        const canvas = document.getElementById('ekgCanvas');
        const ctx = canvas.getContext('2d');
        
        const W = 300, H = 100;
        canvas.width = W;
        canvas.height = H;

        // EKG-Ringpuffer
        const BUFFER_SIZE = W;
        let ekgBuffer = new Array(BUFFER_SIZE).fill(H/2);
        let time = 0;

        function drawGrid() {
            ctx.strokeStyle = '#00ff4110';
            ctx.lineWidth = 0.5;
            for (let x = 0; x < W; x += 30) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, H);
                ctx.strokeStyle = '#00ff4120';
                ctx.stroke();
            }
            for (let y = 0; y < H; y += 20) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(W, y);
                ctx.strokeStyle = '#00ff4120';
                ctx.stroke();
            }
        }

        function generateHeartbeatValue(t) {
            let base = H/2 + Math.sin(t * 0.02) * 3;
            let beat = 0;
            let phase = (t % 80) / 80;
            
            if (phase < 0.1) {
                beat = -15 * (1 - phase*10); 
            } else if (phase < 0.15) {
                beat = -15 + 30 * ((phase-0.1)*20);
            } else if (phase < 0.25) {
                beat = 15 - 25 * ((phase-0.15)*10);
            } else {
                beat = Math.sin(phase * 10) * 2;
            }
            return Math.max(5, Math.min(H-5, base + beat));
        }

        function drawEKG() {
            ctx.fillStyle = '#0a0a0f40';
            ctx.fillRect(0, 0, W, H);
            drawGrid();
            
            ctx.beginPath();
            ctx.strokeStyle = '#00ff41';
            ctx.lineWidth = 1.8;
            ctx.shadowColor = '#00ff41';
            ctx.shadowBlur = 6;
            
            for (let x = 0; x < BUFFER_SIZE; x++) {
                let y = ekgBuffer[x];
                if (x === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = '#00ff41';
            ctx.shadowBlur = 8;
            ctx.beginPath();
            ctx.arc(BUFFER_SIZE-1, ekgBuffer[BUFFER_SIZE-1], 2, 0, 2*Math.PI);
            ctx.fill();
            ctx.shadowBlur = 0;
        }

        function updateEKG() {
            let newValue = generateHeartbeatValue(time);
            ekgBuffer.shift();
            ekgBuffer.push(newValue);
            time++;
            if (time > 100000) time = 0;
        }

        function ekgLoop() {
            updateEKG();
            drawEKG();
            setTimeout(ekgLoop, 50);
        }

        ekgLoop();
    </script>
