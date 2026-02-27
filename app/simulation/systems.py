"""
Infrastructure simulation module.
Simulates servers and operating systems.
No real systems are accessed.
"""

from typing import List, Dict, Any
import uuid


class SystemSimulation:
    """
    Base class for simulated systems/servers.
    """
    
    def __init__(self, hostname: str, os_type: str, os_version: str):
        self.id = f"system_{uuid.uuid4().hex[:8]}"
        self.hostname = hostname
        self.os_type = os_type
        self.os_version = os_version
        self.open_ports: List[int] = []
        self.services: Dict[str, Dict[str, Any]] = {}
        self.vulnerabilities: List[str] = []
        self.misconfigurations: List[str] = []
        self.credentials: Dict[str, str] = {}
        self.permissions: Dict[str, List[str]] = {}
    
    def add_port(self, port: int, service: str, version: str = "latest"):
        """Add an open port with service information."""
        self.open_ports.append(port)
        self.services[str(port)] = {
            "name": service,
            "version": version,
            "status": "running"
        }
    
    def add_vulnerability(self, vuln_type: str):
        """Add a vulnerability to the system."""
        if vuln_type not in self.vulnerabilities:
            self.vulnerabilities.append(vuln_type)
    
    def add_misconfiguration(self, config_issue: str):
        """Add a misconfiguration to the system."""
        if config_issue not in self.misconfigurations:
            self.misconfigurations.append(config_issue)
    
    def set_credentials(self, username: str, password: str):
        """Set system credentials."""
        self.credentials[username] = password
    
    def add_permission(self, user: str, permissions: List[str]):
        """Add user permissions."""
        self.permissions[user] = permissions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert system to dictionary representation."""
        return {
            "id": self.id,
            "hostname": self.hostname,
            "os": {
                "type": self.os_type,
                "version": self.os_version
            },
            "network": {
                "open_ports": self.open_ports,
                "services": self.services
            },
            "security": {
                "vulnerabilities": self.vulnerabilities,
                "misconfigurations": self.misconfigurations,
                "credentials": self.credentials,
                "permissions": self.permissions
            }
        }


class LinuxServer(SystemSimulation):
    """
    Simulated Linux server with common services and configurations.
    """
    
    def __init__(self, hostname: str, distribution: str = "Ubuntu", version: str = "20.04"):
        super().__init__(hostname, "Linux", f"{distribution} {version}")
        self.distribution = distribution
        
        # Default Linux services
        self.add_port(22, "SSH", "OpenSSH 7.6")
        self.add_port(80, "HTTP", "Apache 2.4")
        
        # Default credentials (can be overridden)
        self.set_credentials("root", "password123")
        self.set_credentials("admin", "admin123")
    
    def enable_weak_credentials(self):
        """Enable weak credential configuration."""
        self.add_misconfiguration("default_credentials_enabled")
        self.add_misconfiguration("weak_password_policy")
        self.add_vulnerability("brute_force_ssh")
    
    def enable_outdated_services(self):
        """Enable outdated service versions."""
        self.add_misconfiguration("outdated_services")
        self.add_vulnerability("service_exploitation")
        # Update SSH to vulnerable version
        self.services["22"]["version"] = "OpenSSH 6.6"
    
    def enable_permission_issues(self):
        """Enable permission misconfigurations."""
        self.add_misconfiguration("excessive_permissions")
        self.add_vulnerability("privilege_escalation")
        self.add_permission("www-data", ["sudo", "admin"])


class WebServer(SystemSimulation):
    """
    Simulated web server with HTTP/HTTPS services.
    """
    
    def __init__(self, hostname: str, server_type: str = "Apache"):
        super().__init__(hostname, "Linux", "Ubuntu 20.04")
        self.server_type = server_type
        
        # Web server services
        self.add_port(80, "HTTP", f"{server_type} 2.4")
        self.add_port(443, "HTTPS", f"{server_type} 2.4")
        
        # Default web credentials
        self.set_credentials("webadmin", "admin123")
    
    def enable_insecure_http(self):
        """Enable insecure HTTP configuration."""
        self.add_misconfiguration("http_only")
        self.add_vulnerability("traffic_interception")
    
    def enable_weak_ssl(self):
        """Enable weak SSL/TLS configuration."""
        self.add_misconfiguration("weak_ssl_configuration")
        self.add_vulnerability("ssl_exploitation")
    
    def enable_directory_listing(self):
        """Enable directory listing vulnerability."""
        self.add_misconfiguration("directory_listing_enabled")
        self.add_vulnerability("information_disclosure")


class APIServer(SystemSimulation):
    """
    Simulated API server with REST endpoints.
    """
    
    def __init__(self, hostname: str, api_type: str = "REST"):
        super().__init__(hostname, "Linux", "Ubuntu 20.04")
        self.api_type = api_type
        
        # API server services
        self.add_port(8080, "HTTP-API", "Node.js Express")
        self.add_port(4433, "HTTPS-API", "Node.js Express")
        
        # API credentials
        self.set_credentials("api_user", "api123")
    
    def enable_no_authentication(self):
        """Disable API authentication."""
        self.add_misconfiguration("no_api_authentication")
        self.add_vulnerability("unauthorized_access")
    
    def enable_rate_limiting_disabled(self):
        """Disable API rate limiting."""
        self.add_misconfiguration("no_rate_limiting")
        self.add_vulnerability("api_abuse")
    
    def enable_sensitive_data_exposure(self):
        """Enable sensitive data in API responses."""
        self.add_misconfiguration("sensitive_data_exposure")
        self.add_vulnerability("data_leakage")


class DatabaseServer(SystemSimulation):
    """
    Simulated database server.
    """
    
    def __init__(self, hostname: str, db_type: str = "PostgreSQL"):
        super().__init__(hostname, "Linux", "Ubuntu 20.04")
        self.db_type = db_type
        
        # Database services
        self.add_port(5432, "PostgreSQL", "PostgreSQL 12")
        
        # Database credentials
        self.set_credentials("postgres", "postgres")
        self.set_credentials("db_admin", "admin123")
    
    def enable_default_credentials(self):
        """Enable default database credentials."""
        self.add_misconfiguration("default_db_credentials")
        self.add_vulnerability("unauthorized_db_access")
    
    def enable_public_access(self):
        """Enable public database access."""
        self.add_misconfiguration("public_db_access")
        self.add_vulnerability("remote_db_exploitation")


def linux_server(hostname: str) -> LinuxServer:
    """Factory function for Linux server."""
    return LinuxServer(hostname)


def web_server(hostname: str) -> WebServer:
    """Factory function for web server."""
    return WebServer(hostname)


def api_server(hostname: str) -> APIServer:
    """Factory function for API server."""
    return APIServer(hostname)


def database_server(hostname: str) -> DatabaseServer:
    """Factory function for database server."""
    return DatabaseServer(hostname)


def simulate_systems() -> List[Dict[str, Any]]:
    """
    Generate a default set of simulated systems.
    
    Returns:
        List of system configurations
    """
    systems = []
    
    # Linux server with SSH and HTTP
    linux = linux_server("auth-server")
    linux.enable_weak_credentials()
    systems.append(linux.to_dict())
    
    # Web server with HTTPS
    web = web_server("web-prod")
    web.enable_weak_ssl()
    web.enable_directory_listing()
    systems.append(web.to_dict())
    
    # API server
    api = api_server("api-prod")
    api.enable_no_authentication()
    api.enable_rate_limiting_disabled()
    systems.append(api.to_dict())
    
    return systems