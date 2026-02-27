"""
Database simulation module.
Simulates SQL and NoSQL database environments.
No real databases are accessed.
"""

from typing import List, Dict, Any, Set
import uuid


class DatabaseSimulation:
    """
    Base class for simulated databases.
    """
    
    def __init__(self, name: str, db_type: str, version: str):
        self.id = f"db_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.db_type = db_type
        self.version = version
        self.port: int = 0
        self.host: str = "localhost"
        self.authentication: Dict[str, Any] = {}
        self.roles: Dict[str, Dict[str, Any]] = {}
        self.vulnerabilities: List[str] = []
        self.misconfigurations: List[str] = []
        self.tables: List[Dict[str, Any]] = []
        self.access_logs: List[Dict[str, Any]] = []
    
    def set_connection(self, host: str, port: int):
        """Set database connection parameters."""
        self.host = host
        self.port = port
    
    def set_authentication(self, method: str, enabled: bool = True):
        """Set authentication method."""
        self.authentication = {
            "method": method,
            "enabled": enabled,
            "encryption": "TLS" if enabled else "none"
        }
    
    def add_role(self, role_name: str, permissions: List[str]):
        """Add a database role with permissions."""
        self.roles[role_name] = {
            "permissions": permissions,
            "can_create": False,
            "can_delete": False,
            "can_modify": False
        }
        
        # Set dangerous permissions if role is admin-like
        if "admin" in role_name.lower() or "root" in role_name.lower():
            self.roles[role_name].update({
                "can_create": True,
                "can_delete": True,
                "can_modify": True
            })
    
    def add_vulnerability(self, vuln_type: str):
        """Add a vulnerability to the database."""
        if vuln_type not in self.vulnerabilities:
            self.vulnerabilities.append(vuln_type)
    
    def add_misconfiguration(self, config_issue: str):
        """Add a misconfiguration to the database."""
        if config_issue not in self.misconfigurations:
            self.misconfigurations.append(config_issue)
    
    def add_table(self, table_name: str, columns: List[Dict[str, str]], sensitive_data: bool = False):
        """Add a table to the database."""
        table = {
            "name": table_name,
            "columns": columns,
            "row_count": 1000,
            "sensitive_data": sensitive_data,
            "encrypted": False
        }
        self.tables.append(table)
    
    def log_access(self, user: str, action: str, success: bool, timestamp: str = None):
        """Log database access attempt."""
        from datetime import datetime
        
        log_entry = {
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "user": user,
            "action": action,
            "success": success,
            "source_ip": "192.168.1.100"
        }
        self.access_logs.append(log_entry)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert database to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.db_type,
            "version": self.version,
            "connection": {
                "host": self.host,
                "port": self.port
            },
            "authentication": self.authentication,
            "roles": self.roles,
            "tables": self.tables,
            "security": {
                "vulnerabilities": self.vulnerabilities,
                "misconfigurations": self.misconfigurations
            },
            "logs": self.access_logs[-10:]  # Last 10 log entries
        }


class SQLDatabase(DatabaseSimulation):
    """
    Simulated SQL database (PostgreSQL/MySQL).
    """
    
    def __init__(self, name: str, engine: str = "PostgreSQL", version: str = "12"):
        super().__init__(name, "SQL", f"{engine} {version}")
        self.engine = engine
        self.set_connection("localhost", 5432 if engine == "PostgreSQL" else 3306)
        self.set_authentication("password", True)
        
        # Default roles
        self.add_role("readonly", ["SELECT"])
        self.add_role("readwrite", ["SELECT", "INSERT", "UPDATE"])
        self.add_role("admin", ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"])
        
        # Sample tables
        self.add_table("users", [
            {"name": "id", "type": "INTEGER"},
            {"name": "username", "type": "VARCHAR"},
            {"name": "password_hash", "type": "VARCHAR"},
            {"name": "email", "type": "VARCHAR"}
        ], sensitive_data=True)
        
        self.add_table("orders", [
            {"name": "id", "type": "INTEGER"},
            {"name": "user_id", "type": "INTEGER"},
            {"name": "amount", "type": "DECIMAL"},
            {"name": "status", "type": "VARCHAR"}
        ], sensitive_data=False)
    
    def enable_sql_injection(self):
        """Enable SQL injection vulnerability."""
        self.add_vulnerability("sql_injection")
        self.add_misconfiguration("input_validation_disabled")
    
    def enable_weak_credentials(self):
        """Enable weak database credentials."""
        self.add_misconfiguration("weak_password_policy")
        self.add_vulnerability("brute_force_login")
    
    def enable_excessive_privileges(self):
        """Enable excessive user privileges."""
        self.add_misconfiguration("excessive_privileges")
        self.add_vulnerability("privilege_escalation")
        # Give readonly user dangerous permissions
        if "readonly" in self.roles:
            self.roles["readonly"]["permissions"].extend(["INSERT", "UPDATE", "DELETE"])
    
    def enable_public_access(self):
        """Enable public database access."""
        self.add_misconfiguration("public_access_enabled")
        self.add_vulnerability("unauthorized_access")
        self.host = "0.0.0.0"


class NoSQLDatabase(DatabaseSimulation):
    """
    Simulated NoSQL database (MongoDB).
    """
    
    def __init__(self, name: str, engine: str = "MongoDB", version: str = "4.4"):
        super().__init__(name, "NoSQL", f"{engine} {version}")
        self.engine = engine
        self.set_connection("localhost", 27017)
        self.set_authentication("none", False)  # MongoDB often runs without auth by default
        
        # Default roles
        self.add_role("read", ["find"])
        self.add_role("readWrite", ["find", "insert", "update", "remove"])
        self.add_role("dbAdmin", ["find", "insert", "update", "remove", "createIndex", "drop"])
        
        # Sample collections
        self.add_table("users", [
            {"name": "_id", "type": "ObjectId"},
            {"name": "username", "type": "String"},
            {"name": "email", "type": "String"},
            {"name": "profile", "type": "Object"}
        ], sensitive_data=True)
        
        self.add_table("logs", [
            {"name": "_id", "type": "ObjectId"},
            {"name": "timestamp", "type": "Date"},
            {"name": "level", "type": "String"},
            {"name": "message", "type": "String"}
        ], sensitive_data=False)
    
    def enable_no_auth(self):
        """Enable no authentication."""
        self.add_misconfiguration("authentication_disabled")
        self.add_vulnerability("unauthorized_access")
        self.set_authentication("none", False)
    
    def enable_injection(self):
        """Enable NoSQL injection vulnerability."""
        self.add_vulnerability("nosql_injection")
        self.add_misconfiguration("input_sanitization_disabled")
    
    def enable_excessive_privileges(self):
        """Enable excessive user privileges."""
        self.add_misconfiguration("excessive_privileges")
        self.add_vulnerability("privilege_escalation")
        # Give read user dangerous permissions
        if "read" in self.roles:
            self.roles["read"]["permissions"].extend(["insert", "update", "remove"])


def sql_database(name: str) -> SQLDatabase:
    """Factory function for SQL database."""
    return SQLDatabase(name)


def nosql_database(name: str) -> NoSQLDatabase:
    """Factory function for NoSQL database."""
    return NoSQLDatabase(name)


def simulate_databases() -> List[Dict[str, Any]]:
    """
    Generate a default set of simulated databases.
    
    Returns:
        List of database configurations
    """
    databases = []
    
    # SQL database with vulnerabilities
    sql_db = sql_database("users_db")
    sql_db.enable_sql_injection()
    sql_db.enable_weak_credentials()
    databases.append(sql_db.to_dict())
    
    # NoSQL database with vulnerabilities
    nosql_db = nosql_database("logs_db")
    nosql_db.enable_no_auth()
    nosql_db.enable_excessive_privileges()
    databases.append(nosql_db.to_dict())
    
    return databases
