# Security Policy

## Supported Versions

We provide security updates for the following versions of Genesis ROM Workshop:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ |
| < 1.0   | ❌ (deprecated fake enhancement versions) |

## Reporting a Vulnerability

### Security Contact
Report security vulnerabilities by creating a private GitHub Security Advisory or contacting the maintainers directly.

**Please do NOT create public issues for security vulnerabilities.**

### What We Consider Security Issues

#### **High Priority**
- Code execution vulnerabilities in ROM processing
- Buffer overflows in binary data handling
- Path traversal vulnerabilities in file operations
- Injection vulnerabilities in user input processing

#### **Medium Priority**  
- Information disclosure through ROM analysis
- Denial of service through malformed ROM files
- Privilege escalation in file operations

#### **NOT Security Issues**
- ROM modification capabilities (this is the intended function)
- Ability to analyze copyrighted ROMs (user responsibility)
- Performance issues with large ROM files

### Response Timeline

- **Initial Response:** Within 48 hours
- **Investigation:** Within 1 week  
- **Fix Development:** Within 2 weeks for high priority issues
- **Public Disclosure:** After fix is available and tested

## Security Best Practices for Users

### **ROM File Handling**
- Only analyze ROM files you legally own
- Scan ROM files for malware before processing
- Use the workshop in isolated directories
- Keep backups of original ROM files

### **Installation Security**
```bash
# Verify package integrity
pip install --user -r requirements.txt

# Run in virtual environment (recommended)
python -m venv rom_workshop_env
source rom_workshop_env/bin/activate  # Linux/Mac
# or
rom_workshop_env\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **File System Security**
- Don't run the workshop with administrator privileges
- Use dedicated directories for ROM projects
- Be cautious with network-shared ROM collections
- Validate file paths before processing

## Known Security Considerations

### **ROM Processing Risks**
- **Malformed ROMs:** May cause crashes or unexpected behavior
- **Large ROMs:** May consume significant memory
- **Compressed Data:** Decompression bombs possible in future versions

### **Mitigation Strategies**
- File size limits on ROM processing
- Memory usage monitoring
- Input validation on all ROM data
- Sandboxed processing where possible

### **User Responsibility**
- Legal compliance with ROM ownership
- Respect for intellectual property rights
- Safe computing practices

## Security Features

### **Input Validation**
- ROM format verification before processing
- File size and type checking
- Memory usage limits
- Path traversal prevention

### **Safe Defaults**
- Read-only ROM analysis by default
- Explicit confirmation for ROM modifications
- Automatic backup creation
- Limited file system access

### **Error Handling**
- Graceful failure on malformed ROMs
- Clear error messages without information leakage
- Logging of security-relevant events
- Resource cleanup on errors

## Vulnerability Disclosure Policy

### **Responsible Disclosure**
We follow responsible disclosure practices:

1. **Private reporting** to maintainers
2. **Collaborative investigation** and fix development
3. **Coordinated public disclosure** after fixes are available
4. **Credit to researchers** who report responsibly

### **Public Disclosure Timeline**
- Security fixes will be released before public disclosure
- CVE numbers will be requested for significant vulnerabilities
- Public advisories will include mitigation guidance

## Updates and Notifications

### **Security Updates**
- Released as patch versions (e.g., 1.0.1, 1.0.2)
- Announced in GitHub releases and security advisories
- Include clear upgrade instructions

### **Stay Informed**
- Watch the GitHub repository for security advisories
- Subscribe to release notifications
- Check the changelog for security-related updates

---

**Security is a shared responsibility between the project maintainers and users. We appreciate the security research community's help in keeping Genesis ROM Workshop safe for everyone.**

*This security policy covers the technical tool only. Users are responsible for legal compliance regarding ROM file ownership and usage.*
