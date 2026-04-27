import ast
import sys
import subprocess
import time
import threading

# [Whitelist-based AST Configuration]
ALLOWED_BUILTINS = {
    'print', 'len', 'range', 'sum', 'min', 'max', 'abs', 'sorted', 
    'enumerate', 'zip', 'list', 'dict', 'set', 'tuple', 'int', 'float', 'str', 'bool',
    'isinstance', 'reversed', 'round', 'any', 'all',
    'Exception', 'ValueError', 'TypeError', 'RuntimeError'
}

ALLOWED_MODULES = {
    'math', 'random', 'statistics', 'itertools', 
    'functools', 'collections', 'heapq', 'bisect', 
    'decimal', 'fractions', 'numpy', 'typing', 'datetime', 'time'
}

NUMPY_ALLOWLIST = {
    'array', 'zeros', 'ones', 'arange', 'linspace', 'mean', 'median', 'std', 
    'sum', 'min', 'max', 'dot', 'matmul', 'sqrt', 'abs', 'clip', 'where', 'exp', 'log'
}

DANGEROUS_ATTRIBUTES = {
    'load', 'save', 'savez', 'savez_compressed', 'loadtxt', 'savetxt', 'memmap', 'fromfile'
}

class LocalNameCollector(ast.NodeVisitor):
    def __init__(self):
        self.local_funcs = set()
        
    def visit_FunctionDef(self, node):
        self.local_funcs.add(node.name)
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        self.local_funcs.add(node.name)
        self.generic_visit(node)

class SandboxValidator(ast.NodeVisitor):
    def __init__(self, allowed_locals):
        self.is_valid = True
        self.reason = ""
        self.allowed_locals = allowed_locals
    
    def fail(self, msg):
        self.is_valid = False
        self.reason = msg

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module not in ALLOWED_MODULES:
                self.fail(f"Unauthorized import: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_module = node.module.split('.')[0]
            if base_module not in ALLOWED_MODULES:
                self.fail(f"Unauthorized from-import: {node.module}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in ALLOWED_BUILTINS and func_name not in self.allowed_locals:
                self.fail(f"Unauthorized builtin or external call: {func_name}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Prevent dunder (introspection, classes)
        if node.attr.startswith("__") and node.attr.endswith("__"):
            self.fail(f"Dunder attribute access denied: {node.attr}")
            
        # Explicit Numpy Allowlist
        if isinstance(node.value, ast.Name) and node.value.id in {'np', 'numpy'}:
            if node.attr not in NUMPY_ALLOWLIST:
                self.fail(f"Unauthorized NumPy attribute: numpy.{node.attr}")
        # General dangerous attribute check (fallback)
        elif node.attr in DANGEROUS_ATTRIBUTES:
            self.fail(f"Harmful file IO attribute blocked: {node.attr}")
            
        self.generic_visit(node)

def verify_ast(filepath):
    """
    Allowlist-based 정적 AST 검증.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception as e:
        print(f"[Sandbox] AST Parsing Failed: {e}")
        return False
        
    # Pass 1: 로컬 선언 함수명 식별
    collector = LocalNameCollector()
    collector.visit(tree)
    
    # Pass 2: 화이트리스트 + 로컬 선언 기반 검증
    validator = SandboxValidator(collector.local_funcs)
    validator.visit(tree)
    
    if not validator.is_valid:
        print(f"[Sandbox] Blocked by Policy: {validator.reason}")
        return False
        
    return True

def terminate_and_kill(proc, label="Timeout"):
    """
    자식 프로세스를 단계적으로 자비없이 사살(Kill)합니다.
    """
    if proc.poll() is None:
        proc.terminate()
        time.sleep(0.5)
        if proc.poll() is None:
            proc.kill()
        print(f"\n❌ [Sandbox] Execution aborted cleanly ({label}).")

def run_sandboxed(filepath, timeout=10, max_stdout=100000):
    """
    Piped Streaming을 통한 OOM 방어 및 Wall-clock Timeout 기능.
    """
    if not verify_ast(filepath):
        print("❌ [Sandbox] Code rejected by Validator. Execution aborted.")
        sys.exit(1)
        
    print(f"✅ [Sandbox] Executing isolated process with {timeout}s limit...")
    
    # 프로세스 스폰 (stderr를 stdout으로 결합하여 캡처 제한)
    process = subprocess.Popen(
        [sys.executable, filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    # Wall-clock 타이머 스레드 가동
    timer = threading.Timer(timeout, terminate_and_kill, args=[process, "Timeout 10s Exceeded"])
    timer.start()
    
    stdout_output = ""
    try:
        # Incremental Streaming (블로킹이 걸려도 타이머가 프로세스를 죽이면 해제됨)
        while True:
            chunk = process.stdout.read(4096)
            if not chunk: # EOF
                break
                
            stdout_output += chunk
            if len(stdout_output) > max_stdout:
                stdout_output += "\n...[TRUNCATED STDOUT CAPACITY EXCEEDED]"
                terminate_and_kill(process, "Max Stdout Size Reached")
                break
                
    finally:
        timer.cancel()
        process.stdout.close()
        # 안전한 종료 대기
        process.wait()
        
    print("======== 📦 SANDBOX OUTPUT ========")
    print(stdout_output if stdout_output else "(No Output)")
    
    if process.returncode == 0:
        print("✅ [Sandbox] Completed Successfully.")
    else:
        print(f"❌ [Sandbox] Failed with exit code {process.returncode}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sandbox_runner.py <target_script.py> [timeout_seconds]")
        sys.exit(1)
    
    target_file = sys.argv[1]
    time_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    run_sandboxed(target_file, timeout=time_limit)
