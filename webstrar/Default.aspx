<%@ Page Language="C#" %>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="First National Collegiate Bank of AZ - Accessible banking for everyone. Built by neurodivergent students for financial literacy.">
    <title>First National Collegiate Bank of AZ - Accessible Banking for Everyone</title>
    <style>
        /* === ACCESSIBILITY-FIRST + BISEXUAL PRIDE + KC ROYALS === */
        :root {
            --pink: #D60270;
            --purple: #9B4F96;
            --bi-blue: #0038A8;
            --royals-blue: #004687;
            --powder-blue: #7AB2DD;
            --gold: #BD9B60;
            --white: #FFFFFF;
            --off-white: #F8F9FA;
            --dark: #212529;
            --gradient-pride: linear-gradient(135deg, var(--pink) 0%, var(--purple) 50%, var(--royals-blue) 100%);
            --gradient-light: linear-gradient(135deg, var(--powder-blue) 0%, var(--bi-blue) 100%);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        .skip-link {
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--pink);
            color: var(--white);
            padding: 8px 16px;
            text-decoration: none;
            font-weight: bold;
            z-index: 100;
        }
        .skip-link:focus { top: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: var(--gradient-pride);
            min-height: 100vh;
            background-attachment: fixed;
        }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        header {
            background: var(--white);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
            text-align: center;
            border: 4px solid var(--purple);
        }
        
        h1 {
            background: var(--gradient-pride);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: clamp(1.8rem, 5vw, 3.5rem);
            font-weight: 900;
            margin-bottom: 16px;
        }
        
        .tagline {
            color: var(--royals-blue);
            font-size: clamp(1rem, 3vw, 1.4rem);
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .mission {
            color: var(--purple);
            font-size: clamp(0.9rem, 2.5vw, 1.1rem);
            font-weight: 500;
        }
        
        .content {
            background: var(--white);
            padding: 50px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            border: 4px solid var(--powder-blue);
        }
        
        .section { margin-bottom: 50px; }
        
        h2 {
            color: var(--royals-blue);
            font-size: clamp(1.5rem, 4vw, 2.2rem);
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 4px solid var(--purple);
            font-weight: 800;
        }
        
        .alert {
            background: linear-gradient(135deg, var(--pink), var(--purple));
            color: var(--white);
            padding: 24px;
            border-radius: 12px;
            margin: 30px 0;
            font-size: 1.1rem;
            border: 3px solid var(--royals-blue);
            box-shadow: 0 8px 24px rgba(214, 2, 112, 0.3);
        }
        
        .links {
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .btn {
            padding: 18px 36px;
            background: var(--gradient-pride);
            color: var(--white);
            text-decoration: none;
            border-radius: 50px;
            font-weight: 800;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            border: 3px solid transparent;
            box-shadow: 0 8px 24px rgba(0, 70, 135, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0, 70, 135, 0.4);
            border-color: var(--gold);
        }
        
        .btn:focus {
            outline: 4px solid var(--gold);
            outline-offset: 4px;
        }
        
        .btn-secondary { background: var(--royals-blue); }
        .btn-tertiary { background: var(--purple); }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin: 30px 0;
        }
        
        .feature-card {
            background: linear-gradient(135deg, var(--off-white), var(--white));
            padding: 28px;
            border-radius: 12px;
            border-left: 6px solid var(--pink);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .feature-card:nth-child(2) { border-left-color: var(--purple); }
        .feature-card:nth-child(3) { border-left-color: var(--royals-blue); }
        .feature-card:nth-child(4) { border-left-color: var(--powder-blue); }
        .feature-card:nth-child(5) { border-left-color: var(--bi-blue); }
        .feature-card:nth-child(6) { border-left-color: var(--gold); }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }
        
        .feature-card h3 {
            color: var(--royals-blue);
            margin-bottom: 12px;
            font-size: 1.4rem;
            font-weight: 800;
        }
        
        .security-badges {
            margin: 24px 0;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .security-badge {
            background: var(--royals-blue);
            color: var(--white);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.95rem;
            font-weight: 700;
            border: 2px solid var(--purple);
            transition: all 0.2s ease;
        }
        
        .security-badge:hover {
            background: var(--purple);
            border-color: var(--pink);
            transform: scale(1.05);
        }
        
        ul { margin-left: 24px; line-height: 2.2; }
        li { font-size: 1.05rem; margin-bottom: 8px; }
        li strong { color: var(--royals-blue); font-weight: 800; }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: var(--gradient-light);
            padding: 32px;
            border-radius: 12px;
            text-align: center;
            border: 3px solid var(--white);
            box-shadow: 0 8px 24px rgba(0, 70, 135, 0.2);
        }
        
        .stat-card h3 {
            color: var(--white);
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .stat-card p {
            color: var(--white);
            font-size: 1.1rem;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        .footer {
            text-align: center;
            color: var(--white);
            margin-top: 50px;
            padding: 40px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 16px;
            border: 3px solid var(--powder-blue);
        }
        
        .footer p {
            font-size: 1.1rem;
            margin-bottom: 12px;
            font-weight: 600;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        a { color: var(--royals-blue); font-weight: 700; text-decoration: underline; }
        a:hover { color: var(--pink); }
        a:focus { outline: 3px solid var(--gold); outline-offset: 2px; }
        
        @media (max-width: 768px) {
            .container { padding: 12px; }
            header, .content { padding: 24px; }
            .features { grid-template-columns: 1fr; }
            .links { flex-direction: column; }
            .btn { width: 100%; }
        }
        
        @media (prefers-reduced-motion: reduce) {
            * { animation: none !important; transition: none !important; }
        }
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    
    <div class="container">
        <header role="banner">
            <h1>First National Collegiate Bank of AZ</h1>
            <p class="tagline">Accessible Banking for Everyone</p>
            <p class="mission"><strong>Built by neurodivergent students for financial literacy education</strong></p>
        </header>

        <main id="main-content" class="content" role="main">
            <div class="alert" role="alert">
                <strong>About This Project:</strong> Full-featured banking application deployed as Docker container. Complete source code and documentation in GitHub repository.
            </div>

            <section class="section">
                <h2>Project Resources</h2>
                <nav class="links">
                    <a href="https://github.com/179WestASU/CSE467" class="btn">GitHub Repository</a>
                    <a href="https://github.com/179WestASU/CSE467/blob/main/README.md" class="btn btn-secondary">Documentation</a>
                    <a href="https://github.com/179WestASU/CSE467/blob/main/SECURITY.md" class="btn btn-tertiary">Security Details</a>
                </nav>
            </section>

            <section class="section">
                <h2>All Required Account Types</h2>
                <div class="features">
                    <article class="feature-card">
                        <h3>Savings Account</h3>
                        <p>High-yield savings with 4.25% APY. Perfect for emergency funds and long-term goals.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Checking Account</h3>
                        <p>Daily transactions with 0.01% APY. Debit card access and unlimited transactions.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Certificate of Deposit</h3>
                        <p>6 or 12-month terms with 4.75%-5.25% APY. Fixed-rate, FDIC insured.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Money Market Account</h3>
                        <p>Higher interest at 4.50% APY with limited monthly transactions.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Mutual Fund Deposit</h3>
                        <p>Investment account for mutual fund deposits and portfolio management.</p>
                    </article>
                    <article class="feature-card">
                        <h3>Cash Balance Tracking</h3>
                        <p>Real-time aggregated balance across all accounts with detailed breakdowns.</p>
                    </article>
                </div>
            </section>

            <section class="section">
                <h2>Security Features (CVE-Compliant April 26, 2024)</h2>
                <p><strong>Comprehensive security with all OWASP Top 10 mitigations:</strong></p>
                <div class="security-badges">
                    <span class="security-badge">Argon2id</span>
                    <span class="security-badge">JWT Auth</span>
                    <span class="security-badge">MFA</span>
                    <span class="security-badge">AES-256</span>
                    <span class="security-badge">TLS 1.3</span>
                    <span class="security-badge">SQL Prevention</span>
                    <span class="security-badge">XSS Protection</span>
                    <span class="security-badge">CSRF Tokens</span>
                    <span class="security-badge">Rate Limiting</span>
                    <span class="security-badge">RBAC</span>
                    <span class="security-badge">Audit Logs</span>
                    <span class="security-badge">PCI-DSS</span>
                </div>
            </section>

            <section class="section">
                <h2>Technology Stack</h2>
                <ul>
                    <li><strong>Backend:</strong> Python 3.11, Flask 3.0.3</li>
                    <li><strong>Database:</strong> PostgreSQL 15 with SQLAlchemy ORM</li>
                    <li><strong>Cache:</strong> Redis 7 for rate limiting</li>
                    <li><strong>Security:</strong> Argon2, JWT, PyOTP, Cryptography</li>
                    <li><strong>Deployment:</strong> Docker, Docker Compose, Gunicorn</li>
                </ul>
            </section>

            <section class="section">
                <h2>Project Statistics</h2>
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
                        <p>Documentation Lines</p>
                    </div>
                </div>
            </section>

            <section class="section">
                <h2>Submission Details</h2>
                <ul>
                    <li><strong>Course:</strong> CSE467 - Secure Software Development</li>
                    <li><strong>Repository:</strong> <a href="https://github.com/179WestASU/CSE467">https://github.com/179WestASU/CSE467</a></li>
                    <li><strong>Date:</strong> April 29, 2026 (Late Submission)</li>
                    <li><strong>Status:</strong> Complete - All requirements met</li>
                </ul>
            </section>
        </main>

        <footer class="footer" role="contentinfo">
            <p><strong>First National Collegiate Bank of AZ</strong></p>
            <p>Built by neurodivergent students, for everyone pursuing financial literacy</p>
            <p>&copy; 2026 - Educational Project - CSE467</p>
            <p><em>Accessible. Inclusive. Secure.</em></p>
        </footer>
    </div>
</body>
</html>
