# AI Automated Red Team Agent (AARTA)

An ethical, AI-powered red team simulation system for cybersecurity training and assessment. AARTA provides a safe, offline environment for simulating cyber attacks and analyzing security vulnerabilities.

## 🎯 Project Overview

AARTA is designed for university Tech Innovation Club (TIC) cybersecurity teams to learn and practice red team techniques in a completely safe, simulated environment. **No real hacking, no live targets, no illegal techniques** - everything is simulated and ethical.

### Key Features

- **🔒 Safe & Ethical**: All attacks are simulated logic-based, no real exploits
- **🌐 Offline Operation**: Complete offline functionality, no external dependencies
- **🤖 AI-Powered**: Intelligent attack strategy and reasoning
- **📊 Comprehensive Reporting**: Professional security reports with mitigations
- **🔧 Modular Architecture**: Clean separation between simulation, attack, and analysis components
- **📡 REST API**: Full FastAPI web interface for easy integration

## 🏗️ Architecture

```
ai_red_team_agent/
│
├── app/
│   ├── main.py                     # FastAPI entry point
│   │
│   ├── api/                        # Web API Layer
│   │   ├── routes.py               # API endpoints
│   │   └── schemas.py              # Pydantic data models
│   │
│   ├── core/                       # System Core
│   │   ├── orchestrator.py         # Central execution controller
│   │   ├── state_manager.py        # JSON state persistence
│   │   └── telemetry.py            # Centralized logging
│   │
│   ├── simulation/                 # Infrastructure Simulation (TEAM 1)
│   │   ├── network.py              # Wi-Fi & network simulation
│   │   ├── systems.py              # Server/system simulation
│   │   └── databases.py            # Database simulation
│   │
│   ├── ai_red_team/                # AI Red Team Brain (TEAM 2)
│   │   ├── strategy_engine.py      # Attack planning & reasoning
│   │   ├── attack_library.py       # Simulated attack logic
│   │   └── attack_executor.py      # Executes attacks
│   │
│   ├── analysis/                   # Analysis & Reporting (TEAM 3)
│   │   ├── vulnerability_analyzer.py
│   │   ├── mitigation_engine.py
│   │   └── report_generator.py
│   │
│   └── data/                       # Persistent Data
│       ├── infrastructure.json     # Simulated infrastructure
│       ├── attack_results.json     # Attack outcomes
│       ├── vulnerabilities.json    # Discovered vulnerabilities
│       ├── report.json             # Generated reports
│       └── report.md               # Markdown report
│
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended
- 2GB+ disk space

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_RED_TEAM-AGENT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import fastapi, uvicorn; print('Installation successful!')"
   ```

### Running the Application

#### Method 1: Development Server

```bash
python app/main.py
```

The server will start at `http://localhost:8000`

#### Method 2: Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Method 3: Docker (Optional)

```bash
# Build image
docker build -t aarta .

# Run container
docker run -p 8000:8000 aarta
```

## 📖 Usage Guide

### Web Interface

Once the server is running, access the following endpoints:

- **API Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`
- **System Status**: `http://localhost:8000/api/status`

### Complete Workflow

1. **Simulate Infrastructure**
   ```bash
   curl -X POST "http://localhost:8000/api/infrastructure/simulate" \
        -H "Content-Type: application/json" \
        -d '{"include_rogue_ap": true, "include_vulnerabilities": true}'
   ```

2. **Run Attack Simulation**
   ```bash
   curl -X POST "http://localhost:8000/api/attack/simulate" \
        -H "Content-Type: application/json" \
        -d '{"max_attacks_per_phase": 10}'
   ```

3. **Analyze Vulnerabilities**
   ```bash
   curl -X POST "http://localhost:8000/api/analysis/vulnerabilities" \
        -H "Content-Type: application/json" \
        -d '{"include_cwe_mapping": true, "generate_mitigations": true}'
   ```

4. **Generate Report**
   ```bash
   curl -X POST "http://localhost:8000/api/report/generate" \
        -H "Content-Type: application/json" \
        -d '{"format": "markdown", "include_executive_summary": true}'
   ```

5. **Download Report**
   ```bash
   curl -X GET "http://localhost:8000/api/report/download" -o security_report.md
   ```

### One-Click Full Simulation

Execute the complete workflow in a single call:

```bash
curl -X POST "http://localhost:8000/api/workflow/execute" \
     -H "Content-Type: application/json" \
     -d '{"workflow_type": "full_simulation", "parameters": {"max_attacks_per_phase": 5}}'
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Data Directory
DATA_DIR=app/data

# Logging
LOG_LEVEL=info
LOG_FILE=app/data/logs.log

# Security (Optional)
SECRET_KEY=your-secret-key-here
```

### Customization

#### Infrastructure Simulation

Modify `app/simulation/` files to customize:
- Network types and configurations
- System services and vulnerabilities
- Database setups and misconfigurations

#### Attack Library

Extend `app/ai_red_team/attack_library.py` to add:
- New attack types
- Custom success rate logic
- Additional evidence generation

#### Report Templates

Customize `app/analysis/report_generator.py` for:
- Different report formats
- Custom vulnerability classifications
- Organization-specific templates

## 📊 API Reference

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/infrastructure/simulate` | Simulate infrastructure |
| GET | `/api/infrastructure` | Get current infrastructure |
| POST | `/api/attack/execute` | Execute single attack |
| POST | `/api/attack/simulate` | Run full attack simulation |
| GET | `/api/attack/results` | Get attack results |
| POST | `/api/analysis/vulnerabilities` | Analyze vulnerabilities |
| POST | `/api/report/generate` | Generate security report |
| GET | `/api/report/download` | Download report |
| POST | `/api/workflow/execute` | Execute complete workflow |

### Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": { ... }
}
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### Test Structure

```
tests/
├── test_api.py              # API endpoint tests
├── test_simulation.py       # Infrastructure simulation tests
├── test_attacks.py          # Attack execution tests
├── test_analysis.py         # Vulnerability analysis tests
└── test_integration.py      # End-to-end workflow tests
```

## 🔒 Safety & Ethics

### ✅ What AARTA Does

- Simulates network infrastructure in memory
- Models attack techniques logically
- Generates educational security reports
- Provides safe learning environment

### ❌ What AARTA Doesn't Do

- No real network scanning
- No actual exploitation attempts
- No live system interactions
- No malicious payload generation

### 📋 Ethical Guidelines

1. **Educational Use Only**: Designed for learning and training
2. **No Real Targets**: Never point at real systems or networks
3. **Simulated Environment**: All activities are contained within the application
4. **Responsible Disclosure**: Report vulnerabilities through proper channels

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Install development dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Run tests: `pytest`
6. Submit pull request

### Code Style

- Use Black for formatting: `black app/`
- Use flake8 for linting: `flake8 app/`
- Use mypy for type checking: `mypy app/`

### Team Structure

- **TEAM 1**: Infrastructure & Simulation (`app/simulation/`)
- **TEAM 2**: AI Red Team Brain (`app/ai_red_team/`)
- **TEAM 3**: Analysis & Reporting (`app/analysis/`)

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Port Already in Use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill

# Or use different port
uvicorn app.main:app --port 8001
```

#### Permission Issues
```bash
# Linux/macOS
chmod +x app/main.py

# Windows: Run as Administrator
```

### Debug Mode

Enable debug logging:

```bash
uvicorn app.main:app --log-level debug --reload
```

### Data Issues

Reset all data:

```bash
curl -X DELETE "http://localhost:8000/api/data/reset"
```

## 📚 Learning Resources

### Cybersecurity Fundamentals
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### Red Team Techniques
- [Red Team Operations Handbook](https://www.amazon.com/Red-Team-Operations-Handbook/dp/1119663398)
- [Penetration Testing Basics](https://www.offensive-security.com/)

### Python Security
- [Python Security Practices](https://docs.python.org/3/library/security.html)
- [Secure Coding Guidelines](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## 📄 License

This project is for educational purposes only. See LICENSE file for details.

## 🆘 Support

### Getting Help

1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Search existing issues on GitHub
4. Create new issue with detailed description

### Contact

- Project Maintainers: [TIC Cybersecurity Team]
- Issues: [GitHub Issues]
- Documentation: [Wiki]

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Enhanced AI reasoning engine
- [ ] More attack types
- [ ] Web dashboard UI
- [ ] Real-time attack visualization

### Version 1.2 (Future)
- [ ] Multi-language support
- [ ] Advanced reporting templates
- [ ] Integration with SIEM systems
- [ ] Cloud deployment options

---

**⚠️ Important**: This tool is for educational purposes only. Always ensure you have proper authorization before conducting any security testing, and never use these techniques against systems you don't own or have explicit permission to test.

**🎓 Happy Learning!** 
