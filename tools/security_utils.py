"""
Security Utilities for Genesis ROM Workshop

This module provides security validation and sanitization functions
to prevent common vulnerabilities like path traversal, resource exhaustion,
and symlink attacks.
"""

import os
from pathlib import Path
from typing import Optional


class SecurityError(Exception):
    """Raised when a security validation fails."""
    pass


# Security limits
MAX_ROM_SIZE = 16 * 1024 * 1024  # 16MB (largest Genesis ROM)
MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB
MAX_OUTPUT_FILES = 10000  # Maximum files to create in one operation
MAX_TOTAL_OUTPUT_SIZE = 100 * 1024 * 1024  # 100MB total output
MAX_PATH_LENGTH = 260  # Windows MAX_PATH


def validate_input_path(
    file_path: str,
    must_exist: bool = True,
    allowed_extensions: Optional[list] = None,
    max_size: Optional[int] = None
) -> Path:
    """
    Validate an input file path for security issues.

    Args:
        file_path: Path to validate
        must_exist: Whether file must exist (default: True)
        allowed_extensions: List of allowed file extensions (e.g., ['.bin', '.gen'])
        max_size: Maximum allowed file size in bytes

    Returns:
        Resolved absolute Path object

    Raises:
        SecurityError: If path fails security validation
        FileNotFoundError: If must_exist=True and file doesn't exist
    """
    try:
        path = Path(file_path).resolve(strict=False)
    except (OSError, RuntimeError) as e:
        raise SecurityError(f"Invalid path: {e}")

    # Check path length
    if len(str(path)) > MAX_PATH_LENGTH:
        raise SecurityError(f"Path too long (max {MAX_PATH_LENGTH} characters)")

    # Check for null bytes (common attack vector)
    if '\x00' in str(file_path):
        raise SecurityError("Path contains null bytes")

    # Validate file exists if required
    if must_exist and not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Check if path is a symlink (potential security risk)
    if must_exist and path.is_symlink():
        raise SecurityError(f"Symlinks not allowed: {path}")

    # Validate it's a file, not a directory
    if must_exist and not path.is_file():
        raise SecurityError(f"Not a regular file: {path}")

    # Check file extension
    if allowed_extensions and path.suffix.lower() not in allowed_extensions:
        raise SecurityError(
            f"Invalid file extension '{path.suffix}'. "
            f"Allowed: {', '.join(allowed_extensions)}"
        )

    # Check file size
    if must_exist and max_size:
        file_size = path.stat().st_size
        if file_size > max_size:
            raise SecurityError(
                f"File too large: {file_size:,} bytes "
                f"(max {max_size:,} bytes)"
            )

    return path


def validate_output_path(
    file_path: str,
    base_dir: Optional[str] = None,
    allow_overwrite: bool = False
) -> Path:
    """
    Validate an output file path for security issues.

    Args:
        file_path: Output path to validate
        base_dir: Base directory that output must be within (optional)
        allow_overwrite: Whether to allow overwriting existing files

    Returns:
        Resolved absolute Path object

    Raises:
        SecurityError: If path fails security validation
    """
    try:
        path = Path(file_path).resolve(strict=False)
    except (OSError, RuntimeError) as e:
        raise SecurityError(f"Invalid output path: {e}")

    # Check path length
    if len(str(path)) > MAX_PATH_LENGTH:
        raise SecurityError(f"Output path too long (max {MAX_PATH_LENGTH} characters)")

    # Check for null bytes
    if '\x00' in str(file_path):
        raise SecurityError("Output path contains null bytes")

    # Prevent path traversal - ensure output is within base_dir
    if base_dir:
        base_path = Path(base_dir).resolve(strict=False)
        try:
            path.relative_to(base_path)
        except ValueError:
            raise SecurityError(
                f"Output path must be within {base_dir}. "
                f"Attempted path traversal detected."
            )

    # Check if parent directory exists
    if not path.parent.exists():
        raise SecurityError(f"Output directory does not exist: {path.parent}")

    # Check if we're trying to write to a dangerous location
    dangerous_dirs = ['/etc', '/bin', '/sbin', '/usr/bin', '/System', 'C:\\Windows']
    for dangerous in dangerous_dirs:
        try:
            dangerous_path = Path(dangerous).resolve(strict=False)
            if path.is_relative_to(dangerous_path):
                raise SecurityError(f"Cannot write to system directory: {dangerous}")
        except (ValueError, OSError):
            continue

    # Check if file already exists
    if path.exists():
        if path.is_symlink():
            raise SecurityError(f"Output path is a symlink: {path}")

        if not path.is_file():
            raise SecurityError(f"Output path exists but is not a file: {path}")

        if not allow_overwrite:
            raise SecurityError(f"Output file already exists: {path}")

    return path


def validate_offset_and_length(
    offset: int,
    length: int,
    max_size: int,
    operation_name: str = "operation"
) -> None:
    """
    Validate offset and length parameters to prevent integer overflow and out-of-bounds access.

    Args:
        offset: Starting offset
        length: Length of data
        max_size: Maximum allowed size (e.g., ROM size)
        operation_name: Name of operation for error messages

    Raises:
        SecurityError: If validation fails
    """
    # Check for negative values
    if offset < 0:
        raise SecurityError(f"{operation_name}: offset cannot be negative ({offset})")

    if length < 0:
        raise SecurityError(f"{operation_name}: length cannot be negative ({length})")

    # Check for integer overflow (offset + length)
    try:
        end_position = offset + length
    except OverflowError:
        raise SecurityError(f"{operation_name}: integer overflow in offset + length")

    # Check bounds
    if offset >= max_size:
        raise SecurityError(
            f"{operation_name}: offset {offset} exceeds size {max_size}"
        )

    if end_position > max_size:
        raise SecurityError(
            f"{operation_name}: end position {end_position} exceeds size {max_size}"
        )


def safe_read_file(
    file_path: str,
    max_size: int = MAX_ROM_SIZE,
    allowed_extensions: Optional[list] = None
) -> bytes:
    """
    Safely read a file with size limits and validation.

    Args:
        file_path: Path to file
        max_size: Maximum file size to read
        allowed_extensions: Allowed file extensions

    Returns:
        File contents as bytes

    Raises:
        SecurityError: If validation fails
        IOError: If read fails
    """
    path = validate_input_path(
        file_path,
        must_exist=True,
        allowed_extensions=allowed_extensions,
        max_size=max_size
    )

    try:
        with open(path, 'rb') as f:
            # Read in chunks to avoid reading huge files into memory at once
            data = f.read(max_size + 1)  # Read one extra byte to detect oversized files

            if len(data) > max_size:
                raise SecurityError(
                    f"File exceeds maximum size of {max_size:,} bytes"
                )

            return data

    except IOError as e:
        raise IOError(f"Failed to read file: {e}")


def safe_write_file(
    file_path: str,
    data: bytes,
    base_dir: Optional[str] = None,
    allow_overwrite: bool = True
) -> None:
    """
    Safely write a file with path validation.

    Args:
        file_path: Output path
        data: Data to write
        base_dir: Base directory constraint
        allow_overwrite: Whether to allow overwriting

    Raises:
        SecurityError: If validation fails
        IOError: If write fails
    """
    path = validate_output_path(file_path, base_dir, allow_overwrite)

    # Create parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, 'wb') as f:
            f.write(data)
    except IOError as e:
        raise IOError(f"Failed to write file: {e}")


def validate_extraction_limits(
    files_created: int,
    total_size: int,
    max_files: int = MAX_OUTPUT_FILES,
    max_total_size: int = MAX_TOTAL_OUTPUT_SIZE
) -> None:
    """
    Validate that extraction operations don't exceed resource limits.

    Args:
        files_created: Number of files created so far
        total_size: Total bytes written so far
        max_files: Maximum files allowed
        max_total_size: Maximum total bytes allowed

    Raises:
        SecurityError: If limits exceeded
    """
    if files_created >= max_files:
        raise SecurityError(
            f"Extraction limit reached: {max_files} files. "
            f"Potential disk space exhaustion attack."
        )

    if total_size >= max_total_size:
        raise SecurityError(
            f"Extraction size limit reached: {max_total_size:,} bytes. "
            f"Potential disk space exhaustion attack."
        )


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename to remove dangerous characters.

    Args:
        filename: Original filename
        max_length: Maximum filename length

    Returns:
        Sanitized filename

    Raises:
        SecurityError: If filename is invalid
    """
    if not filename:
        raise SecurityError("Filename cannot be empty")

    # Remove null bytes
    if '\x00' in filename:
        raise SecurityError("Filename contains null bytes")

    # Remove path separators and dangerous characters
    dangerous_chars = ['/', '\\', '..', '\x00', '\n', '\r', '\t']
    sanitized = filename

    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '_')

    # Remove leading/trailing dots and spaces (Windows issues)
    sanitized = sanitized.strip('. ')

    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    if not sanitized:
        raise SecurityError("Filename becomes empty after sanitization")

    return sanitized
