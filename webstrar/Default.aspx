<%@ Page Language="C#" %>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="First National Collegiate Bank of AZ - Accessible banking built by neurodivergent students.">
    <title>First National Collegiate Bank of AZ</title>
    <style>
        /* SAINT Sunglass Lens Tints Color Palette */
        :root {
            --rose-tint: #E85D75;
            --lavender-tint: #A67C9F;
            --slate-tint: #3D5A80;
            --royal-tint: #004687;
            --sky-tint: #7AB2DD;
            --amber-tint: #D4A574;
            --white: #FFFFFF;
            --off-white: #F8F5F2;
            --charcoal: #2B2D42;
            --light-overlay: rgba(255, 255, 255, 0.85);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        .skip-link {
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--slate-tint);
            color: var(--white);
            padding: 8px 16px;
            text-decoration: none;
            font-weight: 600;
            z-index: 100;
        }
        .skip-link:focus { top: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: var(--charcoal);
            background: linear-gradient(180deg, 
                var(--rose-tint) 0%, 
                var(--lavender-tint) 33%, 
                var(--slate-tint) 66%, 
                var(--royal-tint) 100%);
            min-height: 100vh;
            background-attachment: fixed;
        }
        
        .container { max-width: 1300px; margin: 0 auto; padding: 20px; }
        
        /* Header with Rose Lens Tint */
        header {
            background: var(--white);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, 
                var(--rose-tint), 
                var(--lavender-tint), 
                var(--slate-tint));
        }
        
        h1 {
            background: linear-gradient(90deg, 
                var(--rose-tint), 
                var(--lavender-tint), 
                var(--royal-tint));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: clamp(2rem, 5vw, 3.2rem);
            font-weight: 800;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }
        
        .tagline {
            color: var(--royal-tint);
            font-size: clamp(1rem, 3vw, 1.3rem);
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .mission {
            color: var(--slate-tint);
            font-size: 1rem;
            font-weight: 400;
            font-style: italic;
        }
        
        .content {
            background: var(--white);
            padding: 45px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }
        
        .section { 
            margin-bottom: 45px;
            position: relative;
        }
        
        /* Each section with different lens tint overlay */
        .section:nth-child(1) {
            background: linear-gradient(135deg, 
                rgba(232, 93, 117, 0.03), 
                rgba(232, 93, 117, 0.01));
            padding: 25px;
            border-radius: 12px;
        }
        
        .section:nth-child(2) {
            background: linear-gradient(135deg, 
                rgba(166, 124, 159, 0.03), 
                rgba(166, 124, 159, 0.01));
            padding: 25px;
            border-radius: 12px;
        }
        
        .section:nth-child(3) {
            background: linear-gradient(135deg, 
                rgba(61, 90, 128, 0.03), 
                rgba(61, 90, 128, 0.01));
            padding: 25px;
            border-radius: 12px;
        }
        
        .section:nth-child(4) {
            background: linear-gradient(135deg, 
                rgba(122, 178, 221, 0.03), 
                rgba(122, 178, 221, 0.01));
            padding: 25px;
            border-radius: 12px;
        }
        
        h2 {
            color: var(--royal-tint);
            font-size: clamp(1.5rem, 4vw, 2rem);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid currentColor;
            font-weight: 700;
        }
        
        .section:nth-child(1) h2 { color: var(--rose-tint); border-color: var(--rose-tint); }
        .section:nth-child(2) h2 { color: var(--lavender-tint); border-color: var(--lavender-tint); }
        .section:nth-child(3) h2 { color: var(--slate-tint); border-color: var(--slate-tint); }
        .section:nth-child(4) h2 { color: var(--sky-tint); border-color: var(--sky-tint); }
        .section:nth-child(5) h2 { color: var(--royal-tint); border-color: var(--royal-tint); }
        .section:nth-child(6) h2 { color: var(--amber-tint); border-color: var(--amber-tint); }
        
        .note {
            background: rgba(212, 165, 116, 0.08);
            color: var(--charcoal);
            padding: 20px;
            border-radius: 12px;
            margin: 25px 0;
            border-left: 4px solid var(--amber-tint);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        .links {
            display: flex;
            gap: 16px;
            margin: 25px 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        /* Buttons with lens tint theme */
        .btn {
            padding: 14px 32px;
            background: var(--royal-tint);
            color: var(--white);
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            background: var(--slate-tint);
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 70, 135, 0.25);
        }
        
        .btn:focus {
            outline: 3px solid var(--rose-tint);
            outline-offset: 3px;
        }
        
        .btn-rose {
            background: linear-gradient(135deg, var(--rose-tint), var(--lavender-tint));
        }
        
        .btn-lavender {
            background: linear-gradient(135deg, var(--lavender-tint), var(--slate-tint));
        }
        
        /* Feature cards with different lens tints */
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        
        .feature-card {
            background: var(--white);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }
        
        .feature-card:nth-child(1)::before { background: var(--rose-tint); }
        .feature-card:nth-child(2)::before { background: var(--lavender-tint); }
        .feature-card:nth-child(3)::before { background: var(--slate-tint); }
        .feature-card:nth-child(4)::before { background: var(--royal-tint); }
        .feature-card:nth-child(5)::before { background: var(--sky-tint); }
        .feature-card:nth-child(6)::before { background: var(--amber-tint); }
        
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
        }
        
        .feature-card h3 {
            color: var(--royal-tint);
            margin-bottom: 10px;
            font-size: 1.3rem;
            font-weight: 700;
        }
        
        .feature-card:nth-child(1) h3 { color: var(--rose-tint); }
        .feature-card:nth-child(2) h3 { color: var(--lavender-tint); }
        .feature-card:nth-child(3) h3 { color: var(--slate-tint); }
        .feature-card:nth-child(4) h3 { color: var(--royal-tint); }
        .feature-card:nth-child(5) h3 { color: var(--sky-tint); }
        .feature-card:nth-child(6) h3 { color: var(--amber-tint); }
        
        .feature-card p {
            color: var(--charcoal);
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        /* Security badges with lens tint variations */
        .security-badges {
            margin: 20px 0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .security-badge {
            background: var(--slate-tint);
            color: var(--white);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .security-badge:nth-child(4n+1) { background: var(--rose-tint); }
        .security-badge:nth-child(4n+2) { background: var(--lavender-tint); }
        .security-badge:nth-child(4n+3) { background: var(--slate-tint); }
        .security-badge:nth-child(4n+4) { background: var(--royal-tint); }
        
        .security-badge:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        ul { margin-left: 20px; line-height: 2; }
        li { font-size: 1rem; margin-bottom: 6px; }
        li strong { color: var(--royal-tint); font-weight: 700; }
        
        /* Stats with lens tint gradients */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin: 25px 0;
        }
        
        .stat-card {
            padding: 28px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
            color: var(--white);
        }
        
        .stat-card:nth-child(1) { background: linear-gradient(135deg, var(--rose-tint), var(--lavender-tint)); }
        .stat-card:nth-child(2) { background: linear-gradient(135deg, var(--lavender-tint), var(--slate-tint)); }
        .stat-card:nth-child(3) { background: linear-gradient(135deg, var(--slate-tint), var(--royal-tint)); }
        .stat-card:nth-child(4) { background: linear-gradient(135deg, var(--royal-tint), var(--sky-tint)); }
        .stat-card:nth-child(5) { background: linear-gradient(135deg, var(--sky-tint), var(--amber-tint)); }
        .stat-card:nth-child(6) { background: linear-gradient(135deg, var(--amber-tint), var(--rose-tint)); }
        
        .stat-card h3 {
            color: var(--white);
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 6px;
        }
        
        .stat-card p {
            color: var(--white);
            font-size: 1rem;
            font-weight: 600;
        }
        
        .footer {
            text-align: center;
            color: var(--white);
            margin-top: 40px;
            padding: 35px;
            background: rgba(0, 0, 0, 0.15);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }
        
        .footer p {
            font-size: 1rem;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        a { color: var(--royal-tint); font-weight: 600; }
        a:hover { color: var(--lavender-tint); }
        a:focus { outline: 2px solid var(--rose-tint); outline-offset: 2px; }
        
        @media (max-width: 768px) {
            .container { padding: 12px; }
            header, .content { padding: 24px; }
            .section { padding: 20px !important; }
            .features { grid-template-columns: 1fr; }
            .links { flex-direction: column; }
            .btn { width: 100%; }
        }
        
        @media (prefers-reduced-motion: reduce) {
            * { animation: none !important; transition: none !important; }
            .btn::before { display: none; }
        }
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    
    <div class="container">
        <header role="banner">
            <h1>First National Collegiate Bank of AZ</h1>
            <p class="tagline">Banking Built for Everyone</p>
            <p class="mission">Created by neurodivergent students, designed for financial literacy</p>
        </header>

        <main id="main-content" class="content" role="main">
            <div class="note">
                <strong>About This Project:</strong> A complete banking platform with production-ready security and accessibility. Full source code and technical documentation available in our GitHub repository.
            </div>

            <section class="section">
                <h2>Project Resources</h2>
                <nav class="links">
                    <a href="https://github.com/179WestASU/CSE467" class="btn">View Repository</a>
                    <a href="https://github.com/179WestASU/CSE467/blob/main/README.md" class="btn btn-rose">Documentation</a>
                    <a href="https://github.com/179WestASU/CSE467/blob/main/SECURITY.md" class="btn btn-lavender">Security Guide</a>
                </nav>
            </section>

            <section class="section">
                <h2>Account Types</h2>
                <div class="features">
                    <article class="feature-card">
                        <h3>Savings</h3>
                        <p>High-yield savings at 4.25% APY. Build your emergency fund with competitive returns.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Checking</h3>
                        <p>Everyday banking at 0.01% APY. Unlimited transactions with full debit access.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Certificate of Deposit</h3>
                        <p>Fixed terms at 4.75-5.25% APY. Secure 6 or 12-month investments, FDIC insured.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Money Market</h3>
                        <p>Enhanced interest at 4.50% APY. Better returns with limited monthly transactions.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Mutual Funds</h3>
                        <p>Investment account for mutual fund management and portfolio growth strategies.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Balance Tracking</h3>
                        <p>Live aggregated view across all accounts with detailed analytics and insights.</p>
                    </article>
                </div>
            </section>

            <section class="section">
                <h2>Security Features</h2>
                <p><strong>Enterprise-grade security with comprehensive CVE mitigation (April 26, 2024):</strong></p>
                <div class="security-badges">
                    <span class="security-badge">Argon2id Hashing</span>
                    <span class="security-badge">JWT Tokens</span>
                    <span class="security-badge">Multi-Factor Auth</span>
                    <span class="security-badge">AES-256</span>
                    <span class="security-badge">TLS 1.3</span>
                    <span class="security-badge">SQL Prevention</span>
                    <span class="security-badge">XSS Protection</span>
                    <span class="security-badge">CSRF Defense</span>
                    <span class="security-badge">Rate Limiting</span>
                    <span class="security-badge">Role Control</span>
                    <span class="security-badge">Audit Logs</span>
                    <span class="security-badge">PCI Compliant</span>
                </div>
            </section>

            <section class="section">
                <h2>Technology</h2>
                <ul>
                    <li><strong>Backend:</strong> Python 3.11, Flask 3.0.3</li>
                    <li><strong>Database:</strong> PostgreSQL 15 with SQLAlchemy</li>
                    <li><strong>Cache:</strong> Redis 7 for performance</li>
                    <li><strong>Security:</strong> Argon2, JWT, PyOTP, Cryptography</li>
                    <li><strong>Deployment:</strong> Docker, Docker Compose, Gunicorn</li>
                </ul>
            </section>

            <section class="section">
                <h2>Project Metrics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>3,500+</h3>
                        <p>Lines of Code</p>
                    </div>
                    <div class="stat-card">
                        <h3>15+</h3>
                        <p>Security Features</p>
                    </div>
                    <div class="stat-card">
                        <h3>6</h3>
                        <p>Account Types</p>
                    </div>
                    <div class="stat-card">
                        <h3>12+</h3>
                        <p>API Endpoints</p>
                    </div>
                    <div class="stat-card">
                        <h3>11+</h3>
                        <p>CVEs Mitigated</p>
                    </div>
                    <div class="stat-card">
                        <h3>1,500+</h3>
                        <p>Docs Written</p>
                    </div>
                </div>
            </section>

            <section class="section">
                <h2>Submission</h2>
                <ul>
                    <li><strong>Course:</strong> CSE467 - Secure Software Development</li>
                    <li><strong>Repository:</strong> <a href="https://github.com/179WestASU/CSE467">github.com/179WestASU/CSE467</a></li>
                    <li><strong>Submitted:</strong> April 29, 2026</li>
                    <li><strong>Status:</strong> Complete</li>
                </ul>
            </section>
        </main>

        <footer class="footer" role="contentinfo">
            <p><strong>First National Collegiate Bank of AZ</strong></p>
            <p>Built with care by neurodivergent students</p>
            <p>&copy; 2026 Educational Project</p>
            <p><em>Accessible. Thoughtful. Secure.</em></p>
        </footer>
    </div>
</body>
</html>
