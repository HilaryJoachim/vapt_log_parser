Project Overview
Tech Stack: MongoDB + Python (Flask/FastAPI) + Custom Dashboard
Focus:
•	Collect, parse, and normalize logs
•	Store data in MongoDB
•	Match logs with CVE data (NVD/CIRCL APIs)
•	Generate vulnerability alerts & reports
•	Simple dashboard (Python/Flask + HTML/JS frontend)
•	Integrate with SOC’s existing Wazuh setup later (not immediate priority)
Total Duration: ~8 Weeks (active implementation focus)
________________________________________
📅 Detailed Weekly Timeline
Week 1 — Environment Setup & Architecture Finalization(Soc Team)
•	Finalize system architecture (MongoDB-centered)
•	Create project repository and folder structure (backend, scripts, dashboard, config)
•	Set up MongoDB Atlas or local cluster
•	Connect MongoDB with Python (PyMongo or Motor for async ops)
•	Confirm access/log sources with SOC team (Sudarson MV)
•	Deliverable: Working MongoDB-Python connection & validated log source plan
________________________________________
Week 2 — Log Collection Framework(Soc Team)
•	Develop Python script/module for log ingestion from Syslog and Registry Logs
•	Implement connectors (Filebeat/Wazuh agent optional, use file & socket-based ingestion)
•	Design log schema for MongoDB (fields: host, timestamp, OS, software, version, event type)
•	Begin testing with sample logs (Linux + Windows)
•	Deliverable: Log ingestion system storing normalized logs in MongoDB
________________________________________
VAPT Team: 
Starting Date: 4thNov2025
Week 1 — Log Parsing & Normalization(VAPT Team)
•	Build parser engine in Python to extract meaningful fields
•	Normalize into standard JSON (timestamp, host, version, CVE match-ready)
•	Handle structured & unstructured logs using regex/json parsing
•	Store parsed logs in MongoDB (collection: normalized_logs)
•	Deliverable: Parsed and normalized logs stored consistently in DB
________________________________________
Week 2— CVE Database Integration(VAPT Team)
•	Create scheduled task to fetch CVE data from:
o	NVD JSON Feed (weekly sync)
o	CIRCL API (optional fallback)
•	Build MongoDB collections for CVE Database
•	Implement update & version comparison logic
•	Deliverable: Local CVE Database with updated entries & version comparison ready
________________________________________
Week 3— Vulnerability Matching Engine(VAPT Team)
•	Match installed software (from logs) vs CVE database
•	Implement semantic version matching & severity scoring (Critical/High/Medium/Low)
•	Generate JSON alerts for matched vulnerabilities
•	Deliverable: Vulnerability correlation logic operational
________________________________________
Week 4— Alert Management & Reporting(VAPT Team)
•	Store generated alerts in dedicated MongoDB collection
•	Implement filtering by severity, host, or time range
•	Develop Python-based report generator (PDF/JSON export)
•	Deliverable: Working alert and report generation system
________________________________________
Week 5 — Dashboard & Visualization (Phase 1)(VAPT Team)
•	Develop simple dashboard (Python Flask + HTML/JS or Dash)
•	Display:
o	Vulnerable hosts count
o	Top CVEs
o	Severity distribution (pie/bar charts)
•	Enable login/authentication (basic token or Flask-login)
•	Deliverable: Functional basic dashboard fetching data from MongoDB
________________________________________
Grace Period: 2 weeks
________________________________________

Week 8 — Testing, Integration & Final Review
•	End-to-end testing with real logs
•	(Optional) Connect alert output to Wazuh REST API
•	Prepare final demo report + documentation
•	Deliverable: Fully functional Vulnerability Detection Module (MongoDB + Python)
________________________________________



⚙️ Milestone Summary
Milestone	Deliverable	Target Week
Environment & Architecture	MongoDB setup + diagram approval	Week 1(SOC)
Log Collection	Data stored in MongoDB	Week 2(SOC)
Parsing Engine	Normalized JSON logs	Week 1 (4-11-2025 to 7-11-2025) 
CVE Sync	Local CVE DB	Week 2(10-11-2025 to 14-11-2025)
Matching Engine	Alerts generated	Week 3(17-11-2025 to 21-11-2025)
Reports	Report generation tool	Week 4(24-11-2025 to 28-11-2025)
Dashboard (Phase 1)	Visual charts	Week 5(1-12-2025 to 5-12-2025)
Grace Period	2 weeks	(8-12-2025 to 19-12-2025)
Integration	Final testing + review	Week 8(22-12-2025 to 26-12-2025)

