// // // AARTA Frontend JavaScript - Interactive Dashboard

// // // API Configuration
// // const API_BASE_URL = 'http://localhost:8000';

// // // Application State
// // let appState = {
// //     infrastructureLoaded: false,
// //     attacksExecuted: false,
// //     vulnerabilitiesAnalyzed: false,
// //     reportGenerated: false,
// //     currentData: {
// //         infrastructure: null,
// //         attacks: [],
// //         vulnerabilities: [],
// //         report: null
// //     }
// // };

// // // DOM Elements
// // const elements = {
// //     // Buttons
// //     simulateInfraBtn: document.getElementById('simulate-infra'),
// //     runAttacksBtn: document.getElementById('run-attacks'),
// //     analyzeVulnsBtn: document.getElementById('analyze-vulns'),
// //     generateReportBtn: document.getElementById('generate-report'),
// //     runFullWorkflowBtn: document.getElementById('run-full-workflow'),
// //     resetDataBtn: document.getElementById('reset-data'),
// //     proceedToAnalysisBtn: document.getElementById('proceed-to-analysis'),
// //     proceedToReportBtn: document.getElementById('proceed-to-report'),
// //     downloadReportBtn: document.getElementById('download-report'),
// //     viewFullReportBtn: document.getElementById('view-full-report'),
    
// //     // Status displays
// //     infraStatus: document.getElementById('infra-status'),
// //     attackStatus: document.getElementById('attack-status'),
// //     vulnStatus: document.getElementById('vuln-status'),
// //     reportStatus: document.getElementById('report-status'),
    
// //     // Sections
// //     attackResultsSection: document.getElementById('attack-results-section'),
// //     vulnerabilitySection: document.getElementById('vulnerability-section'),
// //     reportSection: document.getElementById('report-section'),
    
// //     // Content containers
// //     attackList: document.getElementById('attack-list'),
// //     vulnerabilityGrid: document.getElementById('vulnerability-grid'),
// //     reportContent: document.getElementById('report-content'),
    
// //     // Summary elements
// //     executionComplete: document.getElementById('execution-complete'),
// //     successfulCount: document.getElementById('successful-count'),
// //     partialCount: document.getElementById('partial-count'),
// //     failedCount: document.getElementById('failed-count'),
// //     analysisSummary: document.getElementById('analysis-summary'),
// //     severityBreakdown: document.getElementById('severity-breakdown'),
// //     reportActions: document.getElementById('report-actions'),
    
// //     // UI elements
// //     loadingOverlay: document.getElementById('loading-overlay'),
// //     loadingText: document.getElementById('loading-text'),
// //     notificationToast: document.getElementById('notification-toast'),
// //     toastIcon: document.getElementById('toast-icon'),
// //     toastMessage: document.getElementById('toast-message'),
// //     toastClose: document.getElementById('toast-close')
// // };

// // // Initialize application
// // document.addEventListener('DOMContentLoaded', function() {
// //     initializeEventListeners();
// //     checkSystemStatus();
// // });

// // // Event Listeners
// // function initializeEventListeners() {
// //     // Control panel buttons
// //     elements.simulateInfraBtn.addEventListener('click', simulateInfrastructure);
// //     elements.runAttacksBtn.addEventListener('click', runAttackSimulation);
// //     elements.analyzeVulnsBtn.addEventListener('click', analyzeVulnerabilities);
// //     elements.generateReportBtn.addEventListener('click', generateReport);
// //     elements.runFullWorkflowBtn.addEventListener('click', runFullWorkflow);
// //     elements.resetDataBtn.addEventListener('click', resetAllData);
    
// //     // Navigation buttons
// //     elements.proceedToAnalysisBtn.addEventListener('click', () => {
// //         showSection('vulnerability-section');
// //         analyzeVulnerabilities();
// //     });
    
// //     elements.proceedToReportBtn.addEventListener('click', () => {
// //         showSection('report-section');
// //         generateReport();
// //     });
    
// //     // Report actions
// //     elements.downloadReportBtn.addEventListener('click', downloadReport);
// //     elements.viewFullReportBtn.addEventListener('click', viewFullReport);
    
// //     // Toast close
// //     elements.toastClose.addEventListener('click', hideNotification);
// // }

// // // API Helper Functions
// // async function apiCall(endpoint, method = 'GET', data = null) {
// //     try {
// //         const options = {
// //             method,
// //             headers: {
// //                 'Content-Type': 'application/json',
// //             }
// //         };
        
// //         if (data) {
// //             options.body = JSON.stringify(data);
// //         }
        
// //         const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
// //         if (!response.ok) {
// //             const errorData = await response.json().catch(() => ({}));
// //             throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
// //         }
        
// //         return await response.json();
// //     } catch (error) {
// //         console.error('API Error:', error);
// //         throw error;
// //     }
// // }

// // // UI Helper Functions
// // function showLoading(message = 'Processing...') {
// //     elements.loadingText.textContent = message;
// //     elements.loadingOverlay.style.display = 'flex';
// // }

// // function hideLoading() {
// //     elements.loadingOverlay.style.display = 'none';
// // }

// // function showNotification(message, type = 'info') {
// //     elements.toastMessage.textContent = message;
// //     elements.toastIcon.className = `toast-icon fas ${getIconForType(type)}`;
// //     elements.notificationToast.className = `notification-toast toast-${type}`;
// //     elements.notificationToast.style.display = 'block';
    
// //     // Auto-hide after 5 seconds
// //     setTimeout(hideNotification, 5000);
// // }

// // function hideNotification() {
// //     elements.notificationToast.style.display = 'none';
// // }

// // function getIconForType(type) {
// //     const icons = {
// //         success: 'fa-check-circle',
// //         error: 'fa-exclamation-circle',
// //         warning: 'fa-exclamation-triangle',
// //         info: 'fa-info-circle'
// //     };
// //     return icons[type] || icons.info;
// // }

// // function showSection(sectionId) {
// //     // Hide all sections
// //     elements.attackResultsSection.style.display = 'none';
// //     elements.vulnerabilitySection.style.display = 'none';
// //     elements.reportSection.style.display = 'none';
    
// //     // Show requested section
// //     const section = document.getElementById(sectionId);
// //     if (section) {
// //         section.style.display = 'block';
// //     }
// // }

// // function updateButtonStates() {
// //     elements.runAttacksBtn.disabled = !appState.infrastructureLoaded;
// //     elements.analyzeVulnsBtn.disabled = !appState.attacksExecuted;
// //     elements.generateReportBtn.disabled = !appState.vulnerabilitiesAnalyzed;
// // }

// // function updateStatusDisplay() {
// //     elements.infraStatus.textContent = appState.infrastructureLoaded ? 'Loaded' : 'Not Loaded';
// //     elements.attackStatus.textContent = appState.attacksExecuted ? `${appState.currentData.attacks.length} Executed` : '0 Executed';
// //     elements.vulnStatus.textContent = appState.vulnerabilitiesAnalyzed ? `${appState.currentData.vulnerabilities.length} Found` : '0 Found';
// //     elements.reportStatus.textContent = appState.reportGenerated ? 'Generated' : 'Not Generated';
// // }

// // // Core Functions
// // async function checkSystemStatus() {
// //     try {
// //         const status = await apiCall('/api/status');
        
// //         // Update state based on status
// //         appState.infrastructureLoaded = status.data.infrastructure.loaded;
// //         appState.attacksExecuted = status.data.attacks.available;
// //         appState.vulnerabilitiesAnalyzed = status.data.vulnerabilities.available;
// //         appState.reportGenerated = status.data.report.generated;
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         // Load existing data if available
// //         if (appState.infrastructureLoaded) {
// //             await loadInfrastructure();
// //         }
// //         if (appState.attacksExecuted) {
// //             await loadAttackResults();
// //         }
// //         if (appState.vulnerabilitiesAnalyzed) {
// //             await loadVulnerabilities();
// //         }
// //         if (appState.reportGenerated) {
// //             await loadReport();
// //         }
        
// //     } catch (error) {
// //         showNotification('Failed to check system status', 'error');
// //     }
// // }

// // async function simulateInfrastructure() {
// //     try {
// //         showLoading('Simulating infrastructure...');
        
// //         const response = await apiCall('/api/infrastructure/simulate', 'POST', {
// //             include_rogue_ap: true,
// //             include_vulnerabilities: true
// //         });
        
// //         appState.currentData.infrastructure = response.data.infrastructure;
// //         appState.infrastructureLoaded = true;
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         showNotification(`Infrastructure simulated: ${response.data.networks_generated} networks, ${response.data.systems_generated} systems, ${response.data.databases_generated} databases`, 'success');
        
// //     } catch (error) {
// //         showNotification(`Infrastructure simulation failed: ${error.message}`, 'error');
// //     } finally {
// //         hideLoading();
// //     }
// // }

// // async function runAttackSimulation() {
// //     try {
// //         showLoading('Running attack simulation...');
        
// //         const response = await apiCall('/api/attack/simulate', 'POST', {
// //             max_attacks_per_phase: 10
// //         });
        
// //         appState.currentData.attacks = response.data.attack_results;
// //         appState.attacksExecuted = true;
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         // Display attack results
// //         displayAttackResults(response.data);
// //         showSection('attack-results-section');
        
// //         showNotification(`Attack simulation completed: ${response.data.successful_attacks} successful, ${response.data.failed_attacks} failed`, 'success');
        
// //     } catch (error) {
// //         showNotification(`Attack simulation failed: ${error.message}`, 'error');
// //     } finally {
// //         hideLoading();
// //     }
// // }

// // async function analyzeVulnerabilities() {
// //     try {
// //         showLoading('Analyzing vulnerabilities...');
        
// //         const response = await apiCall('/api/analysis/vulnerabilities', 'POST', {
// //             include_cwe_mapping: true,
// //             include_owasp_mapping: true,
// //             generate_mitigations: true
// //         });
        
// //         appState.currentData.vulnerabilities = response.data.vulnerabilities;
// //         appState.vulnerabilitiesAnalyzed = true;
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         // Display vulnerabilities
// //         displayVulnerabilities(response.data);
// //         showSection('vulnerability-section');
        
// //         showNotification(`Vulnerability analysis completed: ${response.data.total_vulnerabilities} vulnerabilities found`, 'success');
        
// //     } catch (error) {
// //         showNotification(`Vulnerability analysis failed: ${error.message}`, 'error');
// //     } finally {
// //         hideLoading();
// //     }
// // }

// // async function generateReport() {
// //     try {
// //         showLoading('Generating security report...');
        
// //         const response = await apiCall('/api/report/generate', 'POST', {
// //             format: 'markdown',
// //             include_executive_summary: true,
// //             include_technical_details: true,
// //             include_mitigations: true,
// //             severity_threshold: 'low'
// //         });
        
// //         appState.currentData.report = response.data.report;
// //         appState.reportGenerated = true;
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         // Display report
// //         displayReport(response.data.report);
// //         showSection('report-section');
        
// //         showNotification('Security report generated successfully', 'success');
        
// //     } catch (error) {
// //         showNotification(`Report generation failed: ${error.message}`, 'error');
// //     } finally {
// //         hideLoading();
// //     }
// // }

// // async function runFullWorkflow() {
// //     try {
// //         showLoading('Running complete workflow...');
        
// //         const response = await apiCall('/api/workflow/execute', 'POST', {
// //             workflow_type: 'full_simulation',
// //             parameters: {
// //                 include_rogue_ap: true,
// //                 include_vulnerabilities: true,
// //                 max_attacks_per_phase: 10,
// //                 report_format: 'markdown'
// //             }
// //         });
        
// //         const workflow = response.data.workflow;
        
// //         // Update all states
// //         appState.infrastructureLoaded = true;
// //         appState.attacksExecuted = true;
// //         appState.vulnerabilitiesAnalyzed = true;
// //         appState.reportGenerated = true;
        
// //         // Extract data from workflow
// //         appState.currentData.infrastructure = workflow.result.infrastructure.infrastructure;
// //         appState.currentData.attacks = workflow.result.attacks.attack_results;
// //         appState.currentData.vulnerabilities = workflow.result.analysis.vulnerabilities;
// //         appState.currentData.report = workflow.result.report.report;
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         // Display all results
// //         displayAttackResults(workflow.result.attacks);
// //         displayVulnerabilities(workflow.result.analysis);
// //         displayReport(workflow.result.report.report);
        
// //         // Show attack results first
// //         showSection('attack-results-section');
        
// //         showNotification('Complete workflow executed successfully', 'success');
        
// //     } catch (error) {
// //         showNotification(`Workflow execution failed: ${error.message}`, 'error');
// //     } finally {
// //         hideLoading();
// //     }
// // }

// // async function resetAllData() {
// //     if (!confirm('Are you sure you want to reset all data? This action cannot be undone.')) {
// //         return;
// //     }
    
// //     try {
// //         showLoading('Resetting all data...');
        
// //         await apiCall('/api/data/reset', 'DELETE');
        
// //         // Reset state
// //         appState = {
// //             infrastructureLoaded: false,
// //             attacksExecuted: false,
// //             vulnerabilitiesAnalyzed: false,
// //             reportGenerated: false,
// //             currentData: {
// //                 infrastructure: null,
// //                 attacks: [],
// //                 vulnerabilities: [],
// //                 report: null
// //             }
// //         };
        
// //         // Clear UI
// //         elements.attackList.innerHTML = '';
// //         elements.vulnerabilityGrid.innerHTML = '';
// //         elements.reportContent.innerHTML = '';
// //         elements.executionComplete.style.display = 'none';
// //         elements.analysisSummary.style.display = 'none';
// //         elements.reportActions.style.display = 'none';
        
// //         // Hide sections
// //         showSection('attack-results-section');
// //         elements.attackResultsSection.style.display = 'none';
// //         elements.vulnerabilitySection.style.display = 'none';
// //         elements.reportSection.style.display = 'none';
        
// //         updateButtonStates();
// //         updateStatusDisplay();
        
// //         showNotification('All data has been reset', 'success');
        
// //     } catch (error) {
// //         showNotification(`Data reset failed: ${error.message}`, 'error');
// //     } finally {
// //         hideLoading();
// //     }
// // }

// // // Display Functions
// // function displayAttackResults(data) {
// //     const attacks = data.attack_results;
    
// //     // Clear existing content
// //     elements.attackList.innerHTML = '';
    
// //     // Display each attack
// //     attacks.forEach(attack => {
// //         const attackCard = createAttackCard(attack);
// //         elements.attackList.appendChild(attackCard);
// //     });
    
// //     // Show execution summary
// //     elements.executionComplete.style.display = 'block';
// //     elements.successfulCount.textContent = data.successful_attacks;
// //     elements.partialCount.textContent = '0'; // Not implemented in backend
// //     elements.failedCount.textContent = data.failed_attacks;
// // }

// // function createAttackCard(attack) {
// //     const card = document.createElement('div');
// //     card.className = 'attack-card';
    
// //     const timestamp = new Date(attack.timestamp).toLocaleString();
// //     const successClass = attack.success ? 'attack-success' : 'attack-failed';
// //     const successIcon = attack.success ? 'fa-check' : 'fa-times';
// //     const successText = attack.success ? 'SUCCESS' : 'FAILED';
    
// //     card.innerHTML = `
// //         <div class="attack-header">
// //             <div class="attack-timestamp">
// //                 <i class="fas fa-clock"></i>
// //                 [${timestamp}]
// //             </div>
// //             <div class="${successClass}">
// //                 <i class="fas ${successIcon}"></i>
// //                 ${successText}
// //             </div>
// //         </div>
// //         <div class="attack-details">
// //             <div class="attack-detail">
// //                 <div class="attack-detail-label">Phase:</div>
// //                 <div class="attack-detail-value attack-phase">${getAttackPhase(attack.attack_type)}</div>
// //             </div>
// //             <div class="attack-detail">
// //                 <div class="attack-detail-label">Attack:</div>
// //                 <div class="attack-detail-value">${formatAttackType(attack.attack_type)}</div>
// //             </div>
// //             <div class="attack-detail">
// //                 <div class="attack-detail-label">Target:</div>
// //                 <div class="attack-detail-value">${attack.target}</div>
// //             </div>
// //             <div class="attack-detail">
// //                 <div class="attack-detail-label">Evidence:</div>
// //                 <div class="attack-detail-value">${attack.evidence.join(', ')}</div>
// //             </div>
// //         </div>
// //     `;
    
// //     return card;
// // }

// // function displayVulnerabilities(data) {
// //     const vulnerabilities = data.vulnerabilities;
    
// //     // Clear existing content
// //     elements.vulnerabilityGrid.innerHTML = '';
    
// //     // Display each vulnerability
// //     vulnerabilities.forEach(vuln => {
// //         const vulnCard = createVulnerabilityCard(vuln);
// //         elements.vulnerabilityGrid.appendChild(vulnCard);
// //     });
    
// //     // Show analysis summary
// //     elements.analysisSummary.style.display = 'block';
// //     displaySeverityBreakdown(data.severity_breakdown);
// // }

// // function createVulnerabilityCard(vulnerability) {
// //     const card = document.createElement('div');
// //     card.className = `vulnerability-card ${vulnerability.severity}`;
    
// //     card.innerHTML = `
// //         <div class="vulnerability-header">
// //             <div class="vulnerability-title">${vulnerability.name}</div>
// //             <div class="vulnerability-severity severity-${vulnerability.severity}">${vulnerability.severity}</div>
// //         </div>
// //         <div class="vulnerability-description">${vulnerability.description}</div>
// //         <div class="vulnerability-details">
// //             <div class="vulnerability-detail">
// //                 <div class="vulnerability-detail-label">Target:</div>
// //                 <div class="vulnerability-detail-value">${vulnerability.target}</div>
// //             </div>
// //             <div class="vulnerability-detail">
// //                 <div class="vulnerability-detail-label">Vector:</div>
// //                 <div class="vulnerability-detail-value">${vulnerability.attack_vector}</div>
// //             </div>
// //             ${vulnerability.cwe_id ? `
// //                 <div class="vulnerability-detail">
// //                     <div class="vulnerability-detail-label">CWE:</div>
// //                     <div class="vulnerability-detail-value">${vulnerability.cwe_id}</div>
// //                 </div>
// //             ` : ''}
// //             ${vulnerability.owasp_category ? `
// //                 <div class="vulnerability-detail">
// //                     <div class="vulnerability-detail-label">OWASP:</div>
// //                     <div class="vulnerability-detail-value">${vulnerability.owasp_category}</div>
// //                 </div>
// //             ` : ''}
// //         </div>
// //     `;
    
// //     return card;
// // }

// // function displaySeverityBreakdown(breakdown) {
// //     elements.severityBreakdown.innerHTML = '';
    
// //     Object.entries(breakdown).forEach(([severity, count]) => {
// //         if (count > 0) {
// //             const statCard = document.createElement('div');
// //             statCard.className = `stat-card ${severity}`;
// //             statCard.innerHTML = `
// //                 <div class="stat-number">${count}</div>
// //                 <div class="stat-label">${severity.charAt(0).toUpperCase() + severity.slice(1)}</div>
// //             `;
// //             elements.severityBreakdown.appendChild(statCard);
// //         }
// //     });
// // }

// // function displayReport(report) {
// //     elements.reportContent.innerHTML = `
// //         <div class="report-header">
// //             <h3>Security Assessment Report</h3>
// //             <p><strong>Generated:</strong> ${new Date(report.metadata.generated_at).toLocaleString()}</p>
// //             <p><strong>Session ID:</strong> ${report.metadata.session_id}</p>
// //             <p><strong>Total Vulnerabilities:</strong> ${report.metadata.total_vulnerabilities}</p>
// //         </div>
        
// //         <div class="report-section">
// //             <h4>Executive Summary</h4>
// //             <p>${report.executive_summary}</p>
// //         </div>
        
// //         <div class="report-section">
// //             <h4>Attack Timeline</h4>
// //             <pre>${report.attack_timeline}</pre>
// //         </div>
        
// //         <div class="report-section">
// //             <h4>Technical Findings</h4>
// //             ${report.technical_findings.map(finding => `
// //                 <div class="finding">
// //                     <h5>${finding.title}</h5>
// //                     <p>${finding.content}</p>
// //                 </div>
// //             `).join('')}
// //         </div>
        
// //         <div class="report-section">
// //             <h4>Recommendations</h4>
// //             <pre>${report.recommendations}</pre>
// //         </div>
// //     `;
    
// //     elements.reportActions.style.display = 'flex';
// // }

// // // Helper Functions
// // function getAttackPhase(attackType) {
// //     const phases = {
// //         'port_scan': 'Reconnaissance',
// //         'service_discovery': 'Reconnaissance',
// //         'brute_force': 'Exploitation',
// //         'sql_injection': 'Exploitation',
// //         'authentication_bypass': 'Exploitation',
// //         'privilege_escalation': 'Post-Exploitation',
// //         'lateral_movement': 'Post-Exploitation',
// //         'data_access': 'Post-Exploitation'
// //     };
// //     return phases[attackType] || 'Unknown';
// // }

// // function formatAttackType(attackType) {
// //     return attackType.split('_').map(word => 
// //         word.charAt(0).toUpperCase() + word.slice(1)
// //     ).join(' ');
// // }

// // // Data Loading Functions
// // async function loadInfrastructure() {
// //     try {
// //         const response = await apiCall('/api/infrastructure');
// //         appState.currentData.infrastructure = response.data;
// //     } catch (error) {
// //         console.error('Failed to load infrastructure:', error);
// //     }
// // }

// // async function loadAttackResults() {
// //     try {
// //         const response = await apiCall('/api/attack/results');
// //         appState.currentData.attacks = response.data;
// //         displayAttackResults({ attack_results: response.data, successful_attacks: response.data.filter(a => a.success).length, failed_attacks: response.data.filter(a => !a.success).length });
// //     } catch (error) {
// //         console.error('Failed to load attack results:', error);
// //     }
// // }

// // async function loadVulnerabilities() {
// //     try {
// //         const response = await apiCall('/api/analysis/vulnerabilities');
// //         appState.currentData.vulnerabilities = response.data.vulnerabilities;
// //         displayVulnerabilities(response.data);
// //     } catch (error) {
// //         console.error('Failed to load vulnerabilities:', error);
// //     }
// // }

// // async function loadReport() {
// //     try {
// //         const response = await apiCall('/api/report/content');
// //         appState.currentData.report = response.data;
// //         displayReport(response.data);
// //     } catch (error) {
// //         console.error('Failed to load report:', error);
// //     }
// // }

// // // Report Actions
// // async function downloadReport() {
// //     try {
// //         const response = await fetch(`${API_BASE_URL}/api/report/download`);
// //         const blob = await response.blob();
// //         const url = window.URL.createObjectURL(blob);
// //         const a = document.createElement('a');
// //         a.href = url;
// //         a.download = 'security_report.md';
// //         document.body.appendChild(a);
// //         a.click();
// //         window.URL.revokeObjectURL(url);
// //         document.body.removeChild(a);
        
// //         showNotification('Report downloaded successfully', 'success');
// //     } catch (error) {
// //         showNotification('Failed to download report', 'error');
// //     }
// // }

// // function viewFullReport() {
// //     if (appState.currentData.report) {
// //         const reportContent = JSON.stringify(appState.currentData.report, null, 2);
// //         const newWindow = window.open('', '_blank');
// //         newWindow.document.write(`
// //             <html>
// //                 <head>
// //                     <title>AARTA Security Report</title>
// //                     <style>
// //                         body { font-family: monospace; padding: 20px; background: #1a1a1a; color: #e0e0e0; }
// //                         pre { white-space: pre-wrap; }
// //                     </style>
// //                 </head>
// //                 <body>
// //                     <pre>${reportContent}</pre>
// //                 </body>
// //             </html>
// //         `);
// //     }
// // }

// // AARTA Frontend JavaScript - Interactive Dashboard

// // =============================================
// // API Configuration (FIXED - SAME ORIGIN)
// // =============================================
// const API_BASE_URL = '';  // IMPORTANT: Use same origin

// // Application State
// let appState = {
//     infrastructureLoaded: false,
//     attacksExecuted: false,
//     vulnerabilitiesAnalyzed: false,
//     reportGenerated: false,
//     currentData: {
//         infrastructure: null,
//         attacks: [],
//         vulnerabilities: [],
//         report: null
//     }
// };

// // DOM Elements
// const elements = {
//     simulateInfraBtn: document.getElementById('simulate-infra'),
//     runAttacksBtn: document.getElementById('run-attacks'),
//     analyzeVulnsBtn: document.getElementById('analyze-vulns'),
//     generateReportBtn: document.getElementById('generate-report'),
//     runFullWorkflowBtn: document.getElementById('run-full-workflow'),
//     resetDataBtn: document.getElementById('reset-data'),
//     proceedToAnalysisBtn: document.getElementById('proceed-to-analysis'),
//     proceedToReportBtn: document.getElementById('proceed-to-report'),
//     downloadReportBtn: document.getElementById('download-report'),
//     viewFullReportBtn: document.getElementById('view-full-report'),

//     infraStatus: document.getElementById('infra-status'),
//     attackStatus: document.getElementById('attack-status'),
//     vulnStatus: document.getElementById('vuln-status'),
//     reportStatus: document.getElementById('report-status'),

//     attackResultsSection: document.getElementById('attack-results-section'),
//     vulnerabilitySection: document.getElementById('vulnerability-section'),
//     reportSection: document.getElementById('report-section'),

//     attackList: document.getElementById('attack-list'),
//     vulnerabilityGrid: document.getElementById('vulnerability-grid'),
//     reportContent: document.getElementById('report-content'),

//     executionComplete: document.getElementById('execution-complete'),
//     successfulCount: document.getElementById('successful-count'),
//     partialCount: document.getElementById('partial-count'),
//     failedCount: document.getElementById('failed-count'),
//     analysisSummary: document.getElementById('analysis-summary'),
//     severityBreakdown: document.getElementById('severity-breakdown'),
//     reportActions: document.getElementById('report-actions'),

//     loadingOverlay: document.getElementById('loading-overlay'),
//     loadingText: document.getElementById('loading-text'),
//     notificationToast: document.getElementById('notification-toast'),
//     toastIcon: document.getElementById('toast-icon'),
//     toastMessage: document.getElementById('toast-message'),
//     toastClose: document.getElementById('toast-close')
// };

// // Initialize
// document.addEventListener('DOMContentLoaded', function () {
//     initializeEventListeners();
//     checkSystemStatus();
// });

// // =============================================
// // API HELPER
// // =============================================
// async function apiCall(endpoint, method = 'GET', data = null) {
//     try {
//         const options = {
//             method,
//             headers: { 'Content-Type': 'application/json' }
//         };

//         if (data) {
//             options.body = JSON.stringify(data);
//         }

//         const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

//         if (!response.ok) {
//             const errorData = await response.json().catch(() => ({}));
//             throw new Error(errorData.error || errorData.detail || `HTTP ${response.status}`);
//         }

//         return await response.json();

//     } catch (error) {
//         console.error('API Error:', error);
//         showNotification(error.message, 'error');
//         throw error;
//     }
// }

// // =============================================
// // EVENT LISTENERS
// // =============================================
// function initializeEventListeners() {
//     elements.simulateInfraBtn?.addEventListener('click', simulateInfrastructure);
//     elements.runAttacksBtn?.addEventListener('click', runAttackSimulation);
//     elements.analyzeVulnsBtn?.addEventListener('click', analyzeVulnerabilities);
//     elements.generateReportBtn?.addEventListener('click', generateReport);
//     elements.runFullWorkflowBtn?.addEventListener('click', runFullWorkflow);
//     elements.resetDataBtn?.addEventListener('click', resetAllData);
//     elements.downloadReportBtn?.addEventListener('click', downloadReport);
//     elements.viewFullReportBtn?.addEventListener('click', viewFullReport);
//     elements.toastClose?.addEventListener('click', hideNotification);
// }

// // =============================================
// // UI HELPERS
// // =============================================
// function showLoading(message = 'Processing...') {
//     if (!elements.loadingOverlay) return;
//     elements.loadingText.textContent = message;
//     elements.loadingOverlay.style.display = 'flex';
// }

// function hideLoading() {
//     if (elements.loadingOverlay)
//         elements.loadingOverlay.style.display = 'none';
// }

// function showNotification(message, type = 'info') {
//     if (!elements.notificationToast) return;

//     elements.toastMessage.textContent = message;
//     elements.notificationToast.style.display = 'block';
//     elements.notificationToast.className = `notification-toast toast-${type}`;

//     setTimeout(hideNotification, 4000);
// }

// function hideNotification() {
//     if (elements.notificationToast)
//         elements.notificationToast.style.display = 'none';
// }

// // =============================================
// // CORE LOGIC (UNCHANGED FUNCTIONALLY)
// // =============================================

// async function checkSystemStatus() {
//     try {
//         const status = await apiCall('/api/status');

//         appState.infrastructureLoaded = status.data.infrastructure.loaded;
//         appState.attacksExecuted = status.data.attacks.available;
//         appState.vulnerabilitiesAnalyzed = status.data.vulnerabilities.available;
//         appState.reportGenerated = status.data.report.generated;

//         updateStatusDisplay();

//     } catch (error) {
//         console.warn("System status unavailable");
//     }
// }

// function updateStatusDisplay() {
//     if (elements.infraStatus)
//         elements.infraStatus.textContent = appState.infrastructureLoaded ? 'Loaded' : 'Not Loaded';

//     if (elements.attackStatus)
//         elements.attackStatus.textContent = appState.attacksExecuted ? 'Executed' : 'Not Executed';

//     if (elements.vulnStatus)
//         elements.vulnStatus.textContent = appState.vulnerabilitiesAnalyzed ? 'Analyzed' : 'Not Analyzed';

//     if (elements.reportStatus)
//         elements.reportStatus.textContent = appState.reportGenerated ? 'Generated' : 'Not Generated';
// }

// // =============================================
// // REPORT DOWNLOAD FIXED (Same Origin Safe)
// // =============================================
// async function downloadReport() {
//     try {
//         const response = await fetch(`/api/report/download`);

//         if (!response.ok) {
//             throw new Error("Download failed");
//         }

//         const blob = await response.blob();
//         const url = window.URL.createObjectURL(blob);
//         const a = document.createElement('a');

//         a.href = url;
//         a.download = 'security_report.md';
//         document.body.appendChild(a);
//         a.click();

//         window.URL.revokeObjectURL(url);
//         document.body.removeChild(a);

//         showNotification('Report downloaded successfully', 'success');

//     } catch (error) {
//         showNotification(error.message, 'error');
//     }
// }

// // =============================================
// // VIEW FULL REPORT
// // =============================================
// function viewFullReport() {
//     if (!appState.currentData.report) return;

//     const reportContent = JSON.stringify(appState.currentData.report, null, 2);
//     const newWindow = window.open('', '_blank');

//     newWindow.document.write(`
//         <html>
//             <head>
//                 <title>AARTA Security Report</title>
//                 <style>
//                     body { font-family: monospace; padding: 20px; background: #111; color: #eee; }
//                     pre { white-space: pre-wrap; }
//                 </style>
//             </head>
//             <body>
//                 <pre>${reportContent}</pre>
//             </body>
//         </html>
//     `);
// }

// ===============================
// STATE
// ===============================
let appState = {
    infrastructureLoaded: false,
    attacksExecuted: false,
    vulnerabilitiesAnalyzed: false,
    reportGenerated: false,
    currentData: {
        infrastructure: null,
        attacks: [],
        vulnerabilities: [],
        report: null
    }
};

// ===============================
// HELPER FUNCTIONS
// ===============================
function showLoading(message = "Loading...") {
    const loader = document.getElementById("loadingIndicator");
    loader.textContent = message;
    loader.classList.remove("hidden");
}

function hideLoading() {
    const loader = document.getElementById("loadingIndicator");
    loader.classList.add("hidden");
}

function showNotification(message, type = "info") {
    alert(`${type.toUpperCase()}: ${message}`);
}

function updateStatusDisplay() {
    document.getElementById("infraStatus").textContent = appState.infrastructureLoaded ? "✅" : "❌";
    document.getElementById("attackStatus").textContent = appState.attacksExecuted ? "✅" : "❌";
    document.getElementById("vulnStatus").textContent = appState.vulnerabilitiesAnalyzed ? "✅" : "❌";
    document.getElementById("reportStatus").textContent = appState.reportGenerated ? "✅" : "❌";
}

async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (data) options.body = JSON.stringify(data);

    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return await response.json();
}

// ===============================
// CORE WORKFLOW FUNCTIONS
// ===============================
async function simulateInfrastructure() {
    try {
        showLoading("Simulating infrastructure...");
        await apiCall('/api/infrastructure/simulate', 'POST', {
            include_rogue_ap: true,
            include_vulnerabilities: true
        });
        appState.infrastructureLoaded = true;
        updateStatusDisplay();
        showNotification("Infrastructure simulated successfully", "success");
    } catch (error) {
        showNotification(error.message, "error");
    } finally {
        hideLoading();
    }
}

async function runAttackSimulation() {
    try {
        showLoading("Running attack simulation...");
        await apiCall('/api/attack/simulate', 'POST', { max_attacks_per_phase: 10 });
        appState.attacksExecuted = true;
        updateStatusDisplay();
        showNotification("Attack simulation completed", "success");
    } catch (error) {
        showNotification(error.message, "error");
    } finally {
        hideLoading();
    }
}

async function analyzeVulnerabilities() {
    try {
        showLoading("Analyzing vulnerabilities...");
        await apiCall('/api/analysis/vulnerabilities', 'POST', { include_cwe_mapping: true, include_owasp_mapping: true });
        appState.vulnerabilitiesAnalyzed = true;
        updateStatusDisplay();
        showNotification("Vulnerability analysis completed", "success");
    } catch (error) {
        showNotification(error.message, "error");
    } finally {
        hideLoading();
    }
}

async function generateReport() {
    try {
        showLoading("Generating report...");
        await apiCall('/api/report/generate', 'POST', { format: "markdown" });
        appState.reportGenerated = true;
        updateStatusDisplay();
        showNotification("Report generated", "success");
    } catch (error) {
        showNotification(error.message, "error");
    } finally {
        hideLoading();
    }
}

async function runFullWorkflow() {
    try {
        showLoading("Executing full workflow...");
        await apiCall('/api/workflow/execute', 'POST', { workflow_type: "full_simulation" });
        appState.infrastructureLoaded = true;
        appState.attacksExecuted = true;
        appState.vulnerabilitiesAnalyzed = true;
        appState.reportGenerated = true;
        updateStatusDisplay();
        showNotification("Full workflow executed", "success");
    } catch (error) {
        showNotification(error.message, "error");
    } finally {
        hideLoading();
    }
}

async function resetAllData() {
    try {
        if (!confirm("Reset all data?")) return;
        showLoading("Resetting data...");
        await apiCall('/api/data/reset', 'DELETE');
        appState = {
            infrastructureLoaded: false,
            attacksExecuted: false,
            vulnerabilitiesAnalyzed: false,
            reportGenerated: false,
            currentData: { infrastructure: null, attacks: [], vulnerabilities: [], report: null }
        };
        updateStatusDisplay();
        showNotification("System reset complete", "success");
    } catch (error) {
        showNotification(error.message, "error");
    } finally {
        hideLoading();
    }
}

// ===============================
// EVENT LISTENERS
// ===============================
function initializeEventListeners() {
    document.getElementById("simulateInfraBtn")?.addEventListener('click', simulateInfrastructure);
    document.getElementById("runAttackBtn")?.addEventListener('click', runAttackSimulation);
    document.getElementById("analyzeVulnBtn")?.addEventListener('click', analyzeVulnerabilities);
    document.getElementById("generateReportBtn")?.addEventListener('click', generateReport);
    document.getElementById("runWorkflowBtn")?.addEventListener('click', runFullWorkflow);
    document.getElementById("resetBtn")?.addEventListener('click', resetAllData);
}

// ===============================
// INIT
// ===============================
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    updateStatusDisplay();
});